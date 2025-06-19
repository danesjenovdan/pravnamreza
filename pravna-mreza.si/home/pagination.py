from django.core.paginator import InvalidPage, Page, Paginator
from django.utils.functional import cached_property


class LimitOffsetPaginatorStub:
    """
    Paginator stub that doesn't actually paginate, but just holds info needed
    by LimitOffsetPage.
    """

    def __init__(self, object_list):
        self.object_list = object_list

    @cached_property
    def count(self):
        """Return the total number of objects, across all pages."""
        return Paginator.count.real_func(self)


class LimitOffsetPage(Page):
    """
    Based on Django's Page class, but with limit/offset pagination.
    """

    def __init__(self, object_list, limit, offset, paginator):
        super().__init__(object_list, -1, paginator)
        self.limit = limit
        self.offset = offset

    def __repr__(self):
        return f"<LimitOffsetPage limit={self.limit} offset={self.offset}>"

    def __len__(self):
        return len(self.object_list)

    def has_next(self):
        return self.offset + self.limit < self.paginator.count

    def has_previous(self):
        return self.offset > 0

    def next_page_offset(self):
        return self.offset + self.limit

    def previous_page_offset(self):
        return self.offset - self.limit

    def next_page_number(self):
        raise InvalidPage(
            "LimitOffsetPage is not page-based, call `next_page_offset` instead"
        )

    def previous_page_number(self):
        raise InvalidPage(
            "LimitOffsetPage is not page-based, call `previous_page_offset` instead"
        )

    def start_index(self):
        # Special case, return zero if no items.
        if self.paginator.count == 0:
            return 0
        return self.offset + 1

    def end_index(self):
        if self.has_next():
            return self.offset + self.limit
        return self.paginator.count


def paginate_limit_offset(activities, limit=12, offset=0):
    paginator = LimitOffsetPaginatorStub(activities)
    paged_object_list = activities[offset : offset + limit]
    return LimitOffsetPage(paged_object_list, limit, offset, paginator)
