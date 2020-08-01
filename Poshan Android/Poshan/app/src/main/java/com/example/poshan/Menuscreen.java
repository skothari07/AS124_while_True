package com.example.poshan;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;

import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.BaseAdapter;
import android.widget.GridView;

import android.widget.ImageView;
import android.widget.TextView;


public class Menuscreen extends AppCompatActivity {
    private static int k = -1;
    private static int l = -1;
    String mobile;

    GridView gridView;
    String[] menuNames = {"Profile", "General Info (FAQs)", "Help", "Notifications"};
    int[] menuImages = {R.drawable.profile, R.drawable.diet, R.drawable.helpicon, R.drawable.notificationicon};

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Intent intent = getIntent();
        mobile = intent.getStringExtra("mobile");

        setContentView(R.layout.activity_menuscreen);


        gridView = findViewById(R.id.gridview);

        CustomAdapter customAdapter = new CustomAdapter();
        gridView.setAdapter(customAdapter);
        gridView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {


                if (menuNames[i] == "General Info (FAQs)") {
                    Intent intent1 = new Intent(getApplicationContext(), FAQlist.class);
                    startActivity(intent1);


                }
                if (menuNames[i] == "Notifications") {
                    Intent intent2 = new Intent(getApplicationContext(), NotificationsActivity.class);
                    intent2.putExtra("mobile", mobile);
                    startActivity(intent2);

                }

                if (menuNames[i] == "Help") {
                    Intent i2 = new Intent(Intent.ACTION_VIEW, Uri.parse("tel:181"));
                    startActivity(i2);

                }

            }
        });

    }



    private class CustomAdapter extends BaseAdapter {
        @Override
        public int getCount() {
            return menuImages.length;
        }

        @Override
        public Object getItem(int i) {
            return null;
        }

        @Override
        public long getItemId(int i) {
            return 0;
        }

        @Override
        public View getView(int i, View view, ViewGroup viewGroup) {
            View view1 = getLayoutInflater().inflate(R.layout.row_data, null);
            TextView name = view1.findViewById(R.id.item_name);
            ImageView image = view1.findViewById(R.id.images);

            name.setText(menuNames[i]);
            image.setImageResource(menuImages[i]);
            return view1;


        }
    }


}
