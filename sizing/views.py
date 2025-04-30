from django.shortcuts import render
from .forms import SystemDesignForm, ApplianceFormSet

def design_request(request):
    """
    Renders the sizing form and, on POST, echoes back the submitted data.
    """
    submitted = False
    data = {}
    appliances = []

    if request.method == 'POST':
        design_form = SystemDesignForm(request.POST)
        appliance_formset = ApplianceFormSet(request.POST)
        if design_form.is_valid() and appliance_formset.is_valid():
            submitted = True
            data = design_form.cleaned_data
            appliances = [f.cleaned_data for f in appliance_formset]
    else:
        design_form = SystemDesignForm()
        appliance_formset = ApplianceFormSet()

    return render(request, 'sizing/design_form.html', {
        'design_form': design_form,
        'appliance_formset': appliance_formset,
        'submitted': submitted,
        'data': data,
        'appliances': appliances,
    })
