"""Django practice topic bank."""
DJANGO_TOPICS = [
    {
        "question": "Trace Django's request/response cycle from URL to view.",
        "ideal_topics": "middleware, URLconf, WSGI, views",
        "solution_code": '''# config/urls.py
from django.urls import path, include

urlpatterns = [
    path("api/", include("api.urls")),
]

# Request flow:
# 1. WSGI/ASGI handler builds HttpRequest
# 2. Middleware process_request (top to bottom)
# 3. URL resolver matches path → view callable
# 4. View returns HttpResponse
# 5. Middleware process_response (bottom to top)''',
        "solution_explanation": "Middleware wraps the view; order matters for security, sessions, auth.",
        "hints": "Draw the onion model for middleware layers.",
        "time_estimate_minutes": 15,
    },
    {
        "question": "Write a Django model with constraints, indexes, and Meta options.",
        "ideal_topics": "models, Meta, indexes, constraints",
        "solution_code": '''from django.db import models

class Order(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "-created_at"]),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(total__gte=0), name="total_non_negative"),
        ]
        ordering = ["-created_at"]''',
        "solution_explanation": "Indexes align with query patterns. CheckConstraint enforces rules at DB level.",
        "hints": "Use db_index=True only when needed; prefer explicit Index.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Optimize a view queryset to avoid N+1 queries.",
        "ideal_topics": "select_related, prefetch_related, N+1",
        "solution_code": '''# Bad: N+1 — one query per order's user
# orders = Order.objects.all()

# Good: join user in one query
orders = (
    Order.objects.select_related("user")
    .prefetch_related("items__product")
    .filter(status="pending")
)

for order in orders:
    print(order.user.email)  # no extra query''',
        "solution_explanation": "select_related for FK/O2O (SQL JOIN). prefetch_related for M2M/reverse FK.",
        "hints": "Use django-debug-toolbar or nplusone linter.",
        "time_estimate_minutes": 20,
    },
    {
        "question": "Create a custom manager and queryset for active records.",
        "ideal_topics": "managers, querysets, custom QuerySet",
        "solution_code": '''class ActiveQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

class Article(models.Model):
    title = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    objects = models.Manager.from_queryset(ActiveQuerySet)()

# Usage: Article.objects.active()''',
        "solution_explanation": "Custom querysets encapsulate reusable filters; chainable API.",
        "hints": "as_manager() bridges QuerySet methods to default manager.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Implement function-based view with permission and message handling.",
        "ideal_topics": "FBV, permissions, messages framework",
        "solution_code": '''from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

@login_required
@permission_required("orders.change_order", raise_exception=True)
def approve_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.status = "approved"
    order.save(update_fields=["status"])
    messages.success(request, "Order approved.")
    return redirect("order-detail", order_id=order.id)''',
        "solution_explanation": "Decorators stack outside-in. update_fields limits write columns.",
        "hints": "Use get_object_or_404 for 404 on missing records.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Build a class-based ListView with filtering and pagination.",
        "ideal_topics": "CBV, ListView, pagination",
        "solution_code": '''from django.views.generic import ListView

class OrderListView(ListView):
    model = Order
    template_name = "orders/list.html"
    paginate_by = 25
    context_object_name = "orders"

    def get_queryset(self):
        qs = super().get_queryset().select_related("user")
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs.order_by("-created_at")''',
        "solution_explanation": "Override get_queryset for dynamic filtering; paginate_by handles pages.",
        "hints": "LoginRequiredMixin for CBV auth.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Write a data migration to backfill a new field safely.",
        "ideal_topics": "migrations, RunPython, data migration",
        "solution_code": '''from django.db import migrations

def forwards(apps, schema_editor):
    Order = apps.get_model("shop", "Order")
    for order in Order.objects.filter(status="").iterator():
        order.status = "pending"
        order.save(update_fields=["status"])

class Migration(migrations.Migration):
    dependencies = [("shop", "0002_order_status")]
    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]''',
        "solution_explanation": "Use historical models in migrations; iterator() for large tables.",
        "hints": "Separate schema and data migrations for clarity.",
        "time_estimate_minutes": 20,
    },
    {
        "question": "Configure custom user model with email as USERNAME_FIELD.",
        "ideal_topics": "AUTH_USER_MODEL, custom user, settings",
        "solution_code": '''from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = "email"
    objects = UserManager()

# settings.py: AUTH_USER_MODEL = "accounts.User"''',
        "solution_explanation": "Custom user early avoids painful migrations later.",
        "hints": "Set AUTH_USER_MODEL before first migrate.",
        "time_estimate_minutes": 22,
    },
    {
        "question": "Implement middleware for request ID propagation.",
        "ideal_topics": "middleware, logging, request context",
        "solution_code": '''import uuid
from contextvars import ContextVar

request_id_var: ContextVar[str] = ContextVar("request_id", default="")

class RequestIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        rid = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.request_id = rid
        token = request_id_var.set(rid)
        response = self.get_response(request)
        response["X-Request-ID"] = rid
        request_id_var.reset(token)
        return response''',
        "solution_explanation": "contextvars tie ID to async/thread context for logging.",
        "hints": "Add to MIDDLEWARE after SecurityMiddleware.",
        "time_estimate_minutes": 20,
    },
    {
        "question": "Use select_for_update in a transaction for race-safe updates.",
        "ideal_topics": "transactions, locking, F() expressions",
        "solution_code": '''from django.db import transaction
from django.db.models import F

@transaction.atomic
def decrement_stock(product_id, qty):
    product = (
        Product.objects.select_for_update()
        .get(pk=product_id)
    )
    if product.stock < qty:
        raise ValueError("insufficient stock")
    product.stock = F("stock") - qty
    product.save(update_fields=["stock"])''',
        "solution_explanation": "select_for_update locks row until transaction ends. F() avoids race on read-modify-write.",
        "hints": "Use on_commit for side effects after commit.",
        "time_estimate_minutes": 22,
    },
    {
        "question": "Create Django signals for post_save with idempotent side effects.",
        "ideal_topics": "signals, post_save, on_commit",
        "solution_code": '''from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if not created:
        return

    def enqueue():
        send_confirmation_email(instance.id)

    transaction.on_commit(enqueue)''',
        "solution_explanation": "on_commit ensures email fires only after successful DB commit.",
        "hints": "Avoid heavy work directly in signals; prefer tasks.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Write a custom model field for encrypted text at application level.",
        "ideal_topics": "custom fields, encryption, get_prep_value",
        "solution_code": '''from django.db import models
from cryptography.fernet import Fernet

class EncryptedTextField(models.TextField):
    def __init__(self, *args, key=None, **kwargs):
        self.fernet = Fernet(key)
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value is None:
            return value
        return self.fernet.encrypt(value.encode()).decode()

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.fernet.decrypt(value.encode()).decode()''',
        "solution_explanation": "Custom fields control Python ↔ DB conversion.",
        "hints": "Store key in settings/env, not in code.",
        "time_estimate_minutes": 25,
    },
    {
        "question": "Configure caching for a view with cache_page and vary_on_cookie.",
        "ideal_topics": "caching, cache_page, per-user cache",
        "solution_code": '''from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

@vary_on_cookie
@cache_page(60 * 5)
def dashboard(request):
    ...''',
        "solution_explanation": "cache_page stores full response. vary_on_cookie separates cached entries per session.",
        "hints": "Use low-level cache for fragment caching in templates.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Implement soft delete with a custom manager excluding deleted rows.",
        "ideal_topics": "soft delete, managers, default manager",
        "solution_code": '''class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super().update(is_deleted=True, deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)''',
        "solution_explanation": "Default manager hides deleted; all_objects exposes full set.",
        "hints": "Override delete() on model instance too.",
        "time_estimate_minutes": 20,
    },
    {
        "question": "Build a Form with clean_* validation and model form save.",
        "ideal_topics": "forms, validation, ModelForm",
        "solution_code": '''class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["total", "status"]

    def clean_total(self):
        total = self.cleaned_data["total"]
        if total <= 0:
            raise forms.ValidationError("Total must be positive.")
        return total''',
        "solution_explanation": "Field-level clean_* runs after field validators. Form-level clean() for cross-field.",
        "hints": "Use form.errors in templates; never trust POST data.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Use Django admin with list filters, inlines, and readonly fields.",
        "ideal_topics": "admin, ModelAdmin, inlines",
        "solution_code": '''class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status", "total", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["user__email"]
    readonly_fields = ["created_at"]
    inlines = [OrderItemInline]''',
        "solution_explanation": "Admin is rapid internal tooling; optimize list_display queries.",
        "hints": "autocomplete_fields for FK with large tables.",
        "time_estimate_minutes": 15,
    },
    {
        "question": "Configure database routing for read replicas (conceptual).",
        "ideal_topics": "database routing, replicas, multi-db",
        "solution_code": '''class PrimaryReplicaRouter:
    def db_for_read(self, model, **hints):
        return "replica" if not hints.get("instance") else "default"

    def db_for_write(self, model, **hints):
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        return True''',
        "solution_explanation": "Router directs reads to replica; writes stay on primary.",
        "hints": "Watch replication lag for read-your-writes issues.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Write a Celery task with retry and idempotency key.",
        "ideal_topics": "Celery, retries, idempotency",
        "solution_code": '''from celery import shared_task

@shared_task(bind=True, max_retries=5, autoretry_for=(Exception,))
def process_order(self, order_id, idempotency_key):
    if IdempotencyRecord.objects.filter(key=idempotency_key).exists():
        return "already processed"
    with transaction.atomic():
        IdempotencyRecord.objects.create(key=idempotency_key)
        do_work(order_id)''',
        "solution_explanation": "Idempotency keys prevent duplicate side effects on retry.",
        "hints": "Use task acks_late and visibility timeout carefully.",
        "time_estimate_minutes": 22,
    },
    {
        "question": "Implement API throttling concept in a view decorator.",
        "ideal_topics": "rate limiting, cache, throttling",
        "solution_code": '''def rate_limit(key_func, limit=100, window=60):
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            key = f"rl:{key_func(request)}"
            count = cache.get(key, 0)
            if count >= limit:
                return JsonResponse({"error": "rate limited"}, status=429)
            cache.set(key, count + 1, timeout=window)
            return view(request, *args, **kwargs)
        return wrapper
    return decorator''',
        "solution_explanation": "Sliding/fixed window counters in cache are common edge rate limiters.",
        "hints": "DRF has ScopedRateThrottle built-in.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Use Content Security Policy and security middleware settings.",
        "ideal_topics": "security middleware, CSP, HTTPS",
        "solution_code": '''# settings/production.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
X_FRAME_OPTIONS = "DENY"''',
        "solution_explanation": "Production Django hardens cookies, HTTPS, and clickjacking by default settings.",
        "hints": "django-csp or middleware for Content-Security-Policy headers.",
        "time_estimate_minutes": 14,
    },
]
