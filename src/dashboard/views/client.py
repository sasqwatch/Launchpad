#
# MIT License
#
# Copyright 2017 Launchpad project contributors (see COPYRIGHT.md)
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from dashboard.models import Client
from common.session import LaunchpadSession


def view_client_list(request):
    return render(request, 'client_list.html', {
        'clients': Client.objects.all()
    })


class ClientAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('add', 'Add'))

    class Meta:
        model = Client
        fields = ['title', 'platform', 'cpu']


class ViewClientAdd(View):
    def get(self, request):
        return render(request, 'client_add.html', {
            'form': ClientAddForm()
        })

    def post(self, request):
        form = ClientAddForm(data=request.POST)
        if form.is_valid():
            client = form.save()
            return redirect(reverse('client_view', args=(client.client_id,)))
        else:
            return render(request, 'client_add.html', {
                'form': form
            })


class ViewClient(View):

    def show_client_view(self, request, client_id, extra_context=None):
        client = Client.objects.get(client_id=client_id)
        loader = client.get_loader()
        loader_url = request.build_absolute_uri(reverse('client_loader', args=[client_id]))
        one_liner = loader.get_oneliner(loader_url)
        context = {
            'client': client,
            'one_liner': one_liner
        }
        context.update(extra_context or {})
        return render(request, 'client_view.html', context)

    def get(self, request, client_id):
        return self.show_client_view(request, client_id)

    def post(self, request, client_id):
        try:
            directory_listing = LaunchpadSession.clients[client_id].list_direcotry(request.POST['directory'])
        except KeyError:
            directory_listing = 'Error: client is not connected.'

        return self.show_client_view(request, client_id, {
            'directory_listing': directory_listing
        })