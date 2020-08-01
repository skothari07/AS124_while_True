package com.example.poshan;

import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.ImageButton;
import android.widget.ListView;
import android.widget.TextView;

import java.util.Locale;

public class FAQDescription extends AppCompatActivity {
    private ImageButton mButtonSpeak;
    private TextView mButtonSpeak1;
    private TextToSpeech mTTS;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_f_a_q_description);
        mButtonSpeak = findViewById(R.id.iv_);
        mButtonSpeak1=findViewById(R.id.iv8);
        Intent intent = getIntent();
        String recievedsptext=intent.getExtras().get("send").toString();
        mButtonSpeak1.setText(getResources().getString(Integer.parseInt(recievedsptext)));

        mTTS = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status == TextToSpeech.SUCCESS) {

                    int result = mTTS.setLanguage(new Locale("English"));

                    if (result == TextToSpeech.LANG_MISSING_DATA
                            || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                        Log.e("TTS", "Language not supported");
                    } else {
                        mButtonSpeak.setEnabled(true);
                    }
                } else {
                    Log.e("TTS", "Initialization failed");
                }
            }
        });
        mButtonSpeak.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                speak();
            }
        });

        String recievedprodname=intent.getExtras().get("prodname").toString();
        String[] questions=getResources().getStringArray(Integer.parseInt(recievedprodname));
        ListView listView=findViewById(R.id.listView);
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this,android.R.layout.simple_list_item_1,questions);
        listView.setAdapter(adapter);

    }

    private void speak() {
        String text = mButtonSpeak1.getText().toString();

        mTTS.setPitch(1);
        mTTS.setSpeechRate(0);

        mTTS.speak(text, TextToSpeech.QUEUE_FLUSH, null);
    }
    @Override
    protected void onDestroy() {
        if (mTTS != null) {
            mTTS.stop();
            mTTS.shutdown();
        }

        super.onDestroy();
    }

}
