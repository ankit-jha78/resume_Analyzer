from django import forms

class ResumeForm(forms.Form):
    job_description = forms.CharField(
        label="Job Description",
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "placeholder": "Enter Job Description",
                "class": "w-full rounded-md bg-gray-50 border border-gray-300 text-gray-800 p-3 focus:ring-2 focus:ring-blue-500 focus:outline-none",
            }
        ),
        required=False,   # not all buttons need JD
    )

    resume = forms.FileField(
        label="Upload Resume (PDF)",
        widget=forms.ClearableFileInput(
            attrs={
                "accept": "application/pdf",
                "class": "hidden",  # styled with Tailwind drag-drop container
            }
        ),
        required=False,   # allow buttons like custom question without new upload
    )

    custom_question = forms.CharField(
        label="Any Questions?",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ask a custom question...",
                "class": "w-full rounded-md bg-gray-50 border border-red-400 text-gray-800 p-3 focus:ring-2 focus:ring-blue-500 focus:outline-none",
            }
        ),
        required=False,
    )

    # Hidden field to catch which button is pressed
    action = forms.CharField(widget=forms.HiddenInput(), required=False)
