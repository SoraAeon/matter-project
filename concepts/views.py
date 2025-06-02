from django.shortcuts import render, redirect
from .models import Concept, ConceptChat
from .forms import ConceptForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

@login_required
def create_concept(request):
    if request.method == 'POST':
        form = ConceptForm(request.POST)
        if form.is_valid():
            concept = form.save(commit=False)
            concept.user = request.user
            concept.save()
            return redirect('list_concepts')
    else:
        form = ConceptForm()
    return render(request, 'concepts/create_concept.html', {'form': form})

@login_required
def list_concepts(request):
    concepts = Concept.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'concepts/list_concepts.html', {'concepts': concepts})


@login_required
def detail_concept(request, concept_id):
    concept = Concept.objects.get(id=concept_id)
    response_text = None

    if request.method == 'POST':
        question = request.POST.get('question')
        prompt = f"以下はある人の概念『{concept.title}』に関する情報です：\n{concept.description}\n\nこの概念に対して次のように聞かれました：「{question}」\n\nその概念の視点から答えてください："

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # または "gpt-4"
            messages=[
                {"role": "system", "content": "あなたはその人の概念を代弁する役割です。"},
                {"role": "user", "content": prompt},
            ],
        )
        response_text = response.choices[0].message.content
        # 質問と回答を保存
        ConceptChat.objects.create(
            concept=concept,
            question=question,
            answer=response_text
        )

    # 過去の履歴も取得
    chats = concept.chats.all().order_by('-created_at')

    return render(request, 'concepts/detail_concept.html', {
        'concept': concept,
        'response': response_text,
        'chats': chats
    })


@login_required
def edit_concept(request, concept_id):
    concept = Concept.objects.get(id=concept_id, user=request.user)
    if request.method == 'POST':
        form = ConceptForm(request.POST, instance=concept)
        if form.is_valid():
            form.save()
            return redirect('detail_concept', concept_id=concept.id)
    else:
        form = ConceptForm(instance=concept)
    return render(request, 'concepts/edit_concept.html', {'form': form, 'concept': concept})


@login_required
def delete_concept(request, concept_id):
    concept = Concept.objects.get(id=concept_id, user=request.user)
    if request.method == 'POST':
        concept.delete()
        return redirect('list_concepts')
    return render(request, 'concepts/delete_concept.html', {'concept': concept})
