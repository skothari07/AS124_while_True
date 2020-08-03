package com.example.poshan;
import android.content.Intent;
import android.os.Bundle;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.SimpleAdapter;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import java.util.ArrayList;
import java.util.HashMap;

public class ProfileActivity extends AppCompatActivity {
    ListView listview;
    String mob_no;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);
        Intent intent = getIntent();
        mob_no = intent.getStringExtra("mobile");
        getData();

        listview = (ListView)findViewById(R.id.listView);
    }
    private void getData() {

        String url = Config5.DATA_URL + mob_no;

        StringRequest stringRequest = new StringRequest(url, new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {

                showJSON(response);
            }
        },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(ProfileActivity.this, error.getMessage().toString(), Toast.LENGTH_LONG).show();
                    }
                });

        RequestQueue requestQueue = Volley.newRequestQueue(this);
        requestQueue.add(stringRequest);

    }

    private void showJSON(String response) {
        ArrayList<HashMap<String, String>> list = new ArrayList<HashMap<String, String>>();
        try {
            JSONObject jsonObject = new JSONObject(response);
            JSONArray result = jsonObject.getJSONArray(Config5.JSON_ARRAY);

            for (int i = 0; i < result.length(); i++) {
                JSONObject jo = result.getJSONObject(i);
                String u_fname = "Name: "+jo.getString(Config5.KEY_NAME);
                String u_phone = "Registered No: "+jo.getString(Config5.KEY_PHONE);
                String u_status = "Status: Verified";                 //hard coded since only verified users will be able to log in to the app
                String id = jo.getString(Config5.KEY_ID);

                final HashMap<String, String> employees = new HashMap<>();
                employees.put(Config5.KEY_NAME,u_fname);
                employees.put(Config5.KEY_PHONE, u_phone);
                employees.put(Config5.KEY_STAT, u_status);
                employees.put(Config5.KEY_ID, id);

                list.add(employees);

            }


        } catch (JSONException e) {
            e.printStackTrace();
        }
        ListAdapter adapter = new SimpleAdapter(
                ProfileActivity.this, list, R.layout.activity_my_list,
                new String[]{Config5.KEY_NAME, Config5.KEY_PHONE, Config5.KEY_STAT, Config5.KEY_ID},
                new int[]{R.id.title, R.id.date, R.id.data, R.id.tvid});

        listview.setAdapter(adapter);

    }
}
