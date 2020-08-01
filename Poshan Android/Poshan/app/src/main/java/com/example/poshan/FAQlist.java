package com.example.poshan;
import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;

import android.widget.ListView;

public class FAQlist extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_f_a_qlist);

        String[] questions=getResources().getStringArray(R.array.faqquestions);
        ListView listView=findViewById(R.id.listvw);
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this,android.R.layout.simple_list_item_1,questions);
        listView.setAdapter(adapter);
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int position, long id) {
                int currentprodname=R.array.faq1;
                int sptext=R.string.faq1txt;
                Intent intent =new Intent(FAQlist.this,FAQDescription.class);

                if (position ==  0) {

                    currentprodname=R.array.faq1;
                    sptext=R.string.faq1txt;
                }
                if (position ==  1) {
                    currentprodname=R.array.faq2;
                    sptext=R.string.faq2txt;
                }
                if (position ==  2) {
                    currentprodname=R.array.faq3;
                    sptext=R.string.faq3txt;
                }
                if (position ==  3) {
                    currentprodname=R.array.faq4;
                    sptext=R.string.faq4txt;
                }
                if (position ==  4) {
                    currentprodname=R.array.faq5;
                    sptext=R.string.faq5txt;
                }
                if (position ==  5) {
                    currentprodname=R.array.faq6;
                    sptext=R.string.faq6txt;
                }
                if (position ==  6) {
                    currentprodname=R.array.faq7;
                    sptext=R.string.faq7txt;
                }

                intent.putExtra("prodname",currentprodname);
                intent.putExtra("send",sptext);
                startActivity(intent);
            }
        });

    }
}

