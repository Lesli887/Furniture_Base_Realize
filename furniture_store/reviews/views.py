from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Review
from products.models import Product
from .forms import ReviewForm
from django.contrib import messages


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    existing_review = Review.objects.filter(product=product, user=request.user).first()

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.is_approved = False
            review.save()
            messages.success(request, 'Ваш отзыв успешно добавлен и ожидает модерации!')
            return redirect('products:product_detail', slug=product.slug)
    else:
        form = ReviewForm(instance=existing_review)

    return render(request, 'apps/reviews/review_form.html', {
        'form': form,
        'product': product,
        'form_title': 'Редактировать отзыв' if existing_review else 'Добавить отзыв'
    })


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Отзыв успешно обновлен!')
            return redirect('products:product_detail', slug=review.product.slug)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'apps/reviews/review_form.html', {
        'form': form,
        'product': review.product,
        'form_title': 'Редактировать отзыв'
    })


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_slug = review.product.slug
    review.delete()
    messages.success(request, 'Отзыв успешно удален!')
    return redirect('products:product_detail', slug=product_slug)


def product_reviews(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product, is_approved=True).order_by('-created_at')
    return render(request, 'apps/reviews/product_reviews.html', {
        'product': product,
        'reviews': reviews
    })
