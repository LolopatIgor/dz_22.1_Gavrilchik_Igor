from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from catalog.models import Product, Version
from catalog.forms import ProductForm, VersionForm


class ProductListView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Создаем словарь для текущих версий для каждого продукта
        current_versions = {}
        for product in context['object_list']:
            # Получаем текущую версию для продукта
            current_version = product.versions.filter(is_current=True).first()
            current_versions[product.id] = current_version

        # Передаем текущие версии в контекст
        context['current_versions'] = current_versions
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем текущую версию для текущего продукта
        current_object = context['object']
        current_version = current_object.versions.filter(is_current=True).first()

        # Передаем текущую версию в контекст
        context['current_version'] = current_version

        return context


class CatalogCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        contex_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        contex_data['formset'] = SubjectFormset
        return contex_data


class ContactsPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "contacts.html")


def contacts(request):
    return render(request, 'contacts.html')


class CatalogEditView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        contex_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            contex_data['formset'] = SubjectFormset(self.request.POST, instance=self.object)
        else:
            contex_data['formset'] = SubjectFormset(instance=self.object)

        return contex_data

    def form_valid(self, form):
        # Сохраняем форму и получаем объект продукта
        self.object = form.save()  # исправляем здесь: вызываем метод save()

        # Получаем формсет
        formset = self.get_context_data()['formset']

        # Проверяем, что формсет валиден
        if formset.is_valid():
            # Устанавливаем объект продукта для всех версий в формсете
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)
