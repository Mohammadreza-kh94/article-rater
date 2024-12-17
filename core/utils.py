from django_redis import get_redis_connection


def update_rating_cache(article_id, old_score, new_score):
    redis_client = get_redis_connection("default")
    data = f"{old_score}:{new_score}"
    redis_client.lpush(f"rating:{article_id}", data)
    redis_client.sadd("articles_with_pending_updates", article_id)
