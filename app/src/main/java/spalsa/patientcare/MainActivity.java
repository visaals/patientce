package spalsa.patientcare;

import android.content.DialogInterface;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.text.InputType;
import android.util.Log;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import org.w3c.dom.Text;

public class MainActivity extends AppCompatActivity {

    private boolean loggedIn;
    private Patient patient;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        Button loginButton = findViewById(R.id.login);
        loginButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                login();
            }
        });

        loggedIn = false;
        setText("");
        statusBar();
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

    public void setText(String name) {
        TextView view = findViewById(R.id.text);
        if (name.equals("")) {
            view.setText("Welcome to the PatientCare app please login.");
        }
        else {
            view.setText("Welcome " + name);
        }
    }

    public void login() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Login");

        builder.setMessage("Name");
        // Set up the input
        final EditText input = new EditText(this);
        // Specify the type of input expected; this, for example, sets the input as a password, and will mask the text
        builder.setView(input);

        // Set up the buttons
        builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                setPatient(input.getText().toString());
            }
        });
        builder.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.cancel();
            }
        });

        builder.show();
    }

    public void setPatient(final String patientString) {
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        DatabaseReference myRef = database.getReference("Patients");

        // Read from the database
        myRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                // This method is called once with the initial value and again
                // whenever data at this location is updated.
                try {
                    patient = dataSnapshot.child(patientString).getValue(Patient.class);
                    String value = patient.toString();
                    setText(patientString);
                    loggedIn = true;
                    statusBar();
                    Log.d("FirebaseDebug", "Value is: " + value);
                }
                catch (Exception e) {
                    Toast.makeText(MainActivity.this, patientString + " not found.", Toast.LENGTH_SHORT).show();
                    setText("");
                    loggedIn = false;
                    statusBar();
                    Log.d("FirebaseDebug", "User not found: " + patientString);
                }
            }

            @Override
            public void onCancelled(DatabaseError error) {
                // Failed to read value
                Log.w("FirebaseDebug", "Failed to read value.", error.toException());
            }
        });
    }

    public void statusBar() {
        TextView statusBar = findViewById(R.id.status);
        if(loggedIn) {
            long delay = patient.delay();
            if(delay == 0) {
                statusBar.setText("Your appointment is scheduled for " + patient.stringSchedStart24());
                statusBar.setBackgroundColor(R.color.colorPrimary);
            }
            else if(delay > 0) {
                statusBar.setText("Your " + patient.stringSchedStart24() + " running " + String.valueOf(delay) + " minutes behind");
                statusBar.setBackgroundColor(R.color.colorAccent);
            }
            else {
                statusBar.setText("Your " + patient.stringSchedStart24() + " is availible " + String.valueOf(delay) + " minutes early");
                statusBar.setBackgroundColor(R.color.colorPrimaryDark);
            }
        }
        else {
            statusBar.setText("Login to view status");
            statusBar.setBackgroundColor(R.color.colorPrimary);
        }
    }
}
