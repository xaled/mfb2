class AbstractProvider:
    def __init__(self, base_urls, hidden=False, options=None):
        self.base_urls = base_urls
        self.base_url = base_urls[0]
        self.hidden = hidden
        self.options = options or dict()

    def list_root_pages(self):
        raise NotImplementedError()

    def process_page(self, page_name, args=None, kwargs=None):
        raise NotImplementedError()


class ListElement:
    def __init__(self, page_name, title, type_='item', args=None, kwargs=None, thumbnail_image=None, description=None,
                 icon_image=None, is_video=False, source_url=None):
        self.page_name = page_name
        self.title = title
        self.type_ = type_
        self.args = args
        self.kwargs = kwargs
        self.thumbnail_image = thumbnail_image
        self.description = description
        self.icon_image = icon_image
        self.is_video = is_video
        self.source_url = source_url
