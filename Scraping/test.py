# TODO: complete this class

class PaginationHelper:
    # The constructor takes in an array of items and a integer indicating
    # how many items fit within a single page
    def __init__(self, collection, items_per_page):
        self._itemCollection = collection
        self._itemPerPage = items_per_page
        self._itemCount = len(collection)
        self._pageCount = len(collection) / items_per_page
        if len(collection) % items_per_page > 0:
            self._pageCount += 1

    # returns the number of items within the entire collection
    def item_count(self):
        return self._itemCount

    # returns the number of pages
    def page_count(self):
        return self._pageCount

    # returns the number of items on the current page. page_index is zero based
    # this method should return -1 for page_index values that are out of range
    def page_item_count(self, page_index):
        if page_index < self._pageCount - 1:
            return self._itemPerPage
        elif page_index == self._pageCount - 1:
            return len(self._itemCollection) % self._itemPerPage
        elif page_index >= self._pageCount:
            return -1
        return -1

    # determines what page an item is on. Zero based indexes.
    # this method should return -1 for item_index values that are out of range
    def page_index(self, item_index):
        if item_index > self.item_count() or item_index < 0:
            return -1
        return item_index / self._itemPerPage


x=PaginationHelper([1,2,3,4,5,6],4)
print x.page_index(10)