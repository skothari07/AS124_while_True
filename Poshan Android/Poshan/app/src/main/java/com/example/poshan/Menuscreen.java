package com.example.poshan;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import android.app.Activity;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.res.Configuration;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.BaseAdapter;
import android.widget.GridView;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;
import java.util.Locale;

public class Menuscreen extends AppCompatActivity {
    private static int k = -1;
    private static int l = -1;
    String mobile;

    GridView gridView;
    String[] menuNames = {"Profile", "General Info", "Help", "Notifications"};
    int[] menuNames1 = {R.string.menuitem1, R.string.menuitem2, R.string.menuitem3,R.string.menuitem4};
    int[] menuImages = {R.drawable.profile, R.drawable.faq, R.drawable.help, R.drawable.notification};

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Intent intent = getIntent();
        mobile = intent.getStringExtra("mobile");
        loadLocale();


        setContentView(R.layout.activity_menuscreen);

        ImageButton changelang=findViewById(R.id.settingicon);
        changelang.setOnClickListener( new View.OnClickListener(){
            public void onClick(View view)
            {
                showlanguageDialog();
            }
        });

        gridView = findViewById(R.id.gridview);

        CustomAdapter customAdapter = new CustomAdapter();
        gridView.setAdapter(customAdapter);
        gridView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {

                if (menuNames[i] == "Profile") {
                    Intent intent0 = new Intent(getApplicationContext(), ProfileActivity.class);
                    intent0.putExtra("mobile", mobile);
                    startActivity(intent0);


                }
                if (menuNames[i] == "General Info") {
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

    private void showlanguageDialog() {
        final String[] listItems = {"English", "हिंदी", "मराठी"};
        AlertDialog.Builder mBuilder = new AlertDialog.Builder(Menuscreen.this);
        mBuilder.setTitle("Choose Language");
        mBuilder.setSingleChoiceItems(listItems, -1, new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialogInterface, int i) {
                if (i == 0) {
                    setLocale("en");
                    recreate();
                    k=0;
                    l=0;

                }
                else if (i == 1)
                {
                    setLocale("hi");
                    recreate();
                    k=1;
                    l=1;
                }
                else if(i==2)
                {
                    setLocale("mr");
                    recreate();
                    k=2;l=2;


                }

                dialogInterface.dismiss();
            }

        });

        AlertDialog mDialog=mBuilder.create();

        mDialog.show();
    }

    private void setLocale(String lang )
    {
        Locale locale= new Locale(lang);
        Locale.setDefault(locale);
        Configuration config =new Configuration();
        config.locale=locale;
        getBaseContext().getResources().updateConfiguration(config,getBaseContext().getResources().getDisplayMetrics());

        SharedPreferences.Editor editor=getSharedPreferences("Settings", Context.MODE_PRIVATE).edit();
        editor.putString("My_lang",lang);
        editor.apply();


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
            name.setText(menuNames1[i]);
            image.setImageResource(menuImages[i]);
            return view1;


        }
    }
    public void loadLocale()
    {
        SharedPreferences prefs =getSharedPreferences("Settings", Activity.MODE_PRIVATE);
        String language=prefs.getString("My_lang","");

        setLocale(language);


    }

}
