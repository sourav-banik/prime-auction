from django.contrib import admin
from .models import Product, Bid
import datetime
from django.db.models import Sum, Count
from django.db.models.functions import TruncDay
from django.core.serializers.json import DjangoJSONEncoder
import json


# product model 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "name", "description", "photo", "minimum_bid", "bid_deadline", "created_at", "updated_at") 
    ordering = ("-created_at",)  

    def changelist_view(self, request, extra_context=None):
        auc_created = (
            Product.objects.annotate(date=TruncDay("created_at"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )
        auc_completed = (
            Product.objects.filter(bid_deadline__lt= datetime.datetime.now(datetime.timezone.utc))
            .annotate(date=TruncDay("created_at"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )
        as_json = json.dumps(list(auc_created), cls=DjangoJSONEncoder)
        as_json2 = json.dumps(list(auc_completed), cls=DjangoJSONEncoder) 
        auction_running = Product.objects.filter(bid_deadline__gt= datetime.datetime.now(datetime.timezone.utc)).count()
        auction_value = Product.objects.aggregate(Sum('minimum_bid'))
        extra_context = extra_context or {"auction_running": auction_running, "auction_value": auction_value["minimum_bid__sum"], "chart_data": as_json, "auction_completed": as_json2}
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "product_id", "bider", "ask_price", "created_at", "updated_at")
    ordering = ("-created_at",)  