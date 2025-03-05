# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from transformers import pipeline
from transformers import PegasusTokenizer, PegasusForConditionalGeneration, T5Tokenizer, T5ForConditionalGeneration



class WebscraperPipeline:
    #model
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        fieldName = adapter.field_names()

        #print(adapter.get('ExtractedInformation'))
        #model_name = "google/pegasus-xsum"
        #pegasus_tokenizer = PegasusTokenizer.from_pretrained(model_name)
        #info should hold extracted text
        text = adapter.get('ExtractedInformation')
        print("Original Document size", len(adapter.get('ExtractedInformation')))
        adapter['ExtractedInformation'] = WebscraperPipeline.sumarriseExtractedInformation(text)

        return item
    
    @staticmethod
    def sumarriseExtractedInformation(info):
        model_name = "google/pegasus-xsum"
        pegasus_tokenizer = PegasusTokenizer.from_pretrained(model_name)
        pegasus_model = PegasusForConditionalGeneration.from_pretrained(model_name)

        if isinstance(info, list):
            info = " ".join(info)  # Convert list to string

        tokens = pegasus_tokenizer(info, truncation=True, padding="longest", return_tensors="pt")

        encoded_summary = pegasus_model.generate(
        **tokens,
        max_length=150,  
        min_length=80,    
        length_penalty=2.0,  
        num_beams=5,      
        early_stopping=True
        )

        decoded_summary = pegasus_tokenizer.decode(encoded_summary[0], skip_special_tokens=True)
    
        return decoded_summary

class SaveToDatabase():
    pass
