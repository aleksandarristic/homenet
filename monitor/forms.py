from django import forms

from monitor.models import Device


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'description', 'type', 'first_seen', 'last_seen', 'mac_address', 'manufacturer', 'last_ip']

    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        self.fields['first_seen'].widget.attrs['readonly'] = True
        self.fields['last_seen'].widget.attrs['readonly'] = True
        self.fields['mac_address'].widget.attrs['readonly'] = True
        self.fields['last_ip'].widget.attrs['readonly'] = True
