//Ahmad Mozan


package com.example.proj_app;

import android.os.Bundle;

import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.TextView;

import java.net.*;


public class MainActivity extends AppCompatActivity {

    boolean lights = false; // lights originally off
    boolean blinds = false; // blinds originally off

    private void SendMessage(final String msg){

        Thread thread = new Thread(new Runnable() {
            @Override
            public void run(){
                DatagramSocket  ss = null;
                try{
                    ss = new DatagramSocket();
                    InetAddress host = InetAddress.getByName("127.0.0.1");
                    int port = 1001;
                    byte [] data = msg.getBytes() ;
                    DatagramPacket packet = new DatagramPacket( data, data.length, host, port );
                    ss.send( packet );

                } catch (Exception e) {
                    e.printStackTrace();
                } finally {
                    if( ss !=null){
                        ss.close();
                    }
                }

            }
        });
        thread.start();

    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    public void LTS(View view) {
        if(lights == true){
            lights = false;
            final TextView mtv = (TextView) findViewById(R.id.textView1);
            mtv.setText("Lights Closing...");
            SendMessage("2");
        }

        else{
            lights = true;
            final TextView mtv = (TextView) findViewById(R.id.textView1);
            mtv.setText("Lights Opening...");
            SendMessage("1");
        }
    }

    public void BLD(View view) {
        if(blinds == true){
            blinds = false;
            final TextView mtv = (TextView) findViewById(R.id.textView1);
            mtv.setText("Blinds Closing...");
            SendMessage("6");
        }
        else{
            blinds = true;
            final TextView mtv = (TextView) findViewById(R.id.textView1);
            mtv.setText("Blinds Opening...");
            SendMessage("5");
        }
    }

    public void Hum(View view) {
        final TextView mtv = (TextView) findViewById(R.id.textView1);
        mtv.setText("Getting info...");
        SendMessage("4");
    }

    public void Temp(View view) {
        final TextView mtv = (TextView) findViewById(R.id.textView1);
        mtv.setText("Getting info...");
        SendMessage("3");
    }
}
