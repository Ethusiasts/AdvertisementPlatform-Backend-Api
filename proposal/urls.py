from django.urls import path
from proposal.views import ProposalDetail, Proposals

urlpatterns = [
    path('', Proposals.as_view()),
    path('<int:id>', ProposalDetail.as_view())
]
