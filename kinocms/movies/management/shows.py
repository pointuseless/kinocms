from kinocms.movies.models.schedules.show import Show


def create_show_from_template(show: Show, **kwargs) -> Show:
    """Takes an existing show as an argument and returns a copy of it with kwargs passed"""
    new_show = show
    new_show.show_id = None
    new_show.__dict__ |= kwargs
    return new_show
