from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Phrase
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse
from sentence_transformers import SentenceTransformer, util

class PhraseListView(ListView):
    model = Phrase
    template_name = 'phrase_list.html'  


class PhraseCreateView(CreateView):
    model = Phrase
    template_name = 'phrase_form.html' 
    fields = ['text']

class PhraseUpdateView(UpdateView):
    model = Phrase
    template_name = 'phrase_form.html' 
    fields = ['text'] 

class PhraseDeleteView(DeleteView):
    model = Phrase
    template_name = 'phrase_confirm_delete.html'  
    context_object_name = 'mymodel'  
    success_url = reverse_lazy('phrases') 

class PhraselDetailView(DetailView):
    model = Phrase
    template_name = 'phrase_detail.html'  





class HomePage(TemplateView):
    template_name = 'index.html'


@require_POST
def return_suggestions(request):
    text = request.POST.get('text')
    model = SentenceTransformer('all-MiniLM-L6-v2')

    phrases = []

    for obj in Phrase.objects.all():
        phrases.append(obj.text)

    results = []

    #We will be uniting different numbers of words together (from 3 to 8)
    for number_of_words_in_phrase in range(3,8):
        #Splitting the text into words
        words_list = text.split(' ')
        #Looping throught the words in the words list
        for word_index_in_world_list, word in enumerate(words_list):
            #Setting different offsets, so that different words in a sentence are united together, not just the consequent ones
            for offset in range(5):
                #If the index of the word in a list is such that it should be united with 'number_of_words_in_phrase' previous words
                if word_index_in_world_list in list(range(number_of_words_in_phrase-1,len(words_list),number_of_words_in_phrase)):
                    #Then we form a sentence out of those words
                    sentence = ' '.join(words_list[word_index_in_world_list-(number_of_words_in_phrase-1)+offset:word_index_in_world_list+1+offset])
                    if sentence:

                        #Creating a list of sentences the cosine similarity of which should be compared to each other. we add our preloaded phrasess to the target sentence
                        sentences = phrases + [sentence]
                        paraphrases = util.paraphrase_mining(model, sentences)
                        #At this point, the model has computed the similarity of all sentences in the list "sentences"
                        #We loop through top 20 of those comparisons (which are sorted by similarity in descending order)
                        for paraphrase in paraphrases[0:20]:
                            #Getting the score, index 'u' of sentence 1 and index 'y' of sentence 2
                            score, u, y = paraphrase
                            #We set a similarity threshold of 0.43 which must be exceed
                            #We also make sure that we are not comparing the preloaded phrases to each other
                            if score > 0.43 and not (sentences[u] in phrases and sentences[y] in phrases):

                                if sentences[u] == sentence:
                                    results.append([score,sentences[u],sentences[y]])
                                else:
                                    results.append([score,sentences[y],sentences[u]])


                                print("{} \t\t {} \t\t Score: {:.4f}".format(sentences[u], sentences[y], score))

    new_results = []


    #Here we remove all the text phrases that include words from 2 sentences which does not make sense
    for i in results:
        word = i[1]
        if '. ' not in word:
            new_results.append(i)
    
    results = new_results

    considered_words = []
    max_scores = {}
    updated_results = []

    #A text phrase can be repeated in the results. We only keep that result where a text phrase has maximum similarity with a standard phrase
    for sublist in results:
        word = sublist[1]
        score = sublist[0]
        if word in max_scores:
            if score > max_scores[word]:
                max_scores[word] = score
        else:
            max_scores[word] = score
        
        
    

    #We also remove text phrases that are similar. We consider both inclusion of one text phrase inside another and use the model again to remove those with high semantic similarity as well
    #This is done to provide only a single best replacement for one text phrase

    for sublist in results:
        word = sublist[1]
        score = sublist[0]
        should_append = True
        if score == max_scores[word]:
            for w in considered_words:
                
                similar_words = False
                
                word_paraphrases = util.paraphrase_mining(model, [word,w])

                for paraphrase in word_paraphrases[0:]:
                    score, i, j = paraphrase
                    if score > 0.5:
                        similar_words = True
                        break
                    
                if word in w or w in word or similar_words: 
                        
                    should_append = False
                    break
                    
            if should_append:
                considered_words.append(word)
                updated_results.append(sublist)

    
  
    return JsonResponse({'results':updated_results})

