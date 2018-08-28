from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request


class MmPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print(item)
        yield Request(item['images_url'], meta={'name': item['images_path']})

    def file_path(self, request, response=None, info=None):
        image_guid = request.meta['name']
        # 设置图片存放位置，现在设置的为"E://mm/full/2200"
        filename = u'full/{0}'.format(image_guid)
        print("保存成功")
        return filename

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]      # ok判断是否下载成功
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

