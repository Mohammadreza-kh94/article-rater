from celery import shared_task
from django.db import transaction
from django_redis import get_redis_connection

from core.models import Article


@shared_task
def apply_rating_updates():
    redis_client = get_redis_connection("default")

    article_ids = redis_client.smembers("articles_with_pending_updates")
    if not article_ids:
        return

    article_ids = [int(aid) for aid in article_ids]

    for article_id in article_ids:
        key = f"rating:{article_id}"
        updates_data = redis_client.lrange(key, 0, -1)
        if not updates_data:
            redis_client.srem("articles_with_pending_updates", article_id)
            redis_client.delete(key)
            continue

        ratings_count_delta = 0
        ratings_sum_delta = 0

        for update_data in updates_data:
            update_str = update_data.decode("utf-8")
            old_score_str, new_score_str = update_str.split(":", 1)
            new_score = int(new_score_str)

            if old_score_str == "None":
                ratings_count_delta += 1
                ratings_sum_delta += new_score
            else:
                old_score = int(old_score_str)
                ratings_sum_delta += new_score - old_score

        with transaction.atomic():
            article = Article.objects.select_for_update().get(id=article_id)
            article.ratings_count += ratings_count_delta
            article.ratings_sum += ratings_sum_delta
            article.save()

        redis_client.srem("articles_with_pending_updates", article_id)
        redis_client.delete(key)
