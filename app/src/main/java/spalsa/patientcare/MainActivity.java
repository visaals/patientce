package spalsa.patientcare;

import android.content.DialogInterface;
import android.os.Bundle;

import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;

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

import java.util.Calendar;
import java.util.Date;


public class MainActivity extends AppCompatActivity {

    private boolean loggedIn;
    private String patientString;
    private Patient patient;
    private DatabaseReference myRef;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        patientString = "";
        loggedIn = false;

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

        Button checkinButton = findViewById(R.id.checkin);
        checkinButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                checkIn();
            }
        });

        Button clockOutButton = findViewById(R.id.checkout);
        clockOutButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                checkOut();
            }
        });

        setText();
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
        if (id == R.id.help) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    public void setText() {
        TextView view = findViewById(R.id.text);
        if (loggedIn) {
            view.setText("Welcome " + patientString);
        }
        else {
            view.setText("Welcome to the PatientCare app please login.");
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
                patientString = input.getText().toString();
                setPatient();
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

    public void setPatient() {
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        myRef = database.getReference("Patients");

        // Read from the database
        myRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                // This method is called once with the initial value and again
                // whenever data at this location is updated.
                try {
                    if(patientString.equals("")) throw new Exception();
                    patient = dataSnapshot.child(patientString).getValue(Patient.class);
                    String value = patient.toString();
                    loggedIn = true;
                    setText();
                    statusBar();
                    Log.d("FirebaseDebug", "Value is: " + value);
                }
                catch (Exception e) {
                    Toast.makeText(MainActivity.this, patientString + " not found.", Toast.LENGTH_SHORT).show();
                    loggedIn = false;
                    setText();
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
            if (patient.isDone == 1 || patient.isCheckedIn == 1) {
                statusBar.setText("Thank you for arriving");
                        statusBar.setBackgroundResource(R.color.colorPrimary);
            }
            else if (patient.isCancelled == 1) {
                statusBar.setText("Please call (585) 362 9050 to reschedule");
                        statusBar.setBackgroundResource(R.color.ohno);
            }
            else if(delay == 0) {
                statusBar.setText("Your appointment is scheduled for " + patient.stringSchedStart24());
                statusBar.setBackgroundResource(R.color.colorPrimary);
            }
            else if(delay > 0) {
                statusBar.setText("Your " + patient.stringSchedStart24() + " is delayed to " + patient.stringEarliestCome24());
                statusBar.setBackgroundResource(R.color.colorAccent);
            }
            else {
                statusBar.setText("Your " + patient.stringSchedStart24() + " is available at " + patient.stringEarliestCome24());
                statusBar.setBackgroundResource(R.color.colorPrimaryDark);
            }
        }
        else {
            statusBar.setText("Login to view status");
            statusBar.setBackgroundResource(R.color.colorPrimary);
        }
    }

    public void checkIn() {
        if(loggedIn) {
            try {
                if (patient.isCheckedIn == 0) {
                    myRef.child(patientString).child("isCheckedIn").setValue(1);
                    myRef.child(patientString).child("start24").setValue(getTime());
                    myRef.child(patientString).child("end24").setValue(addThirtyMinutes(getTime()));
                }
            }
            catch (Exception e) {
                Log.d("TimeDebug", e.toString());
            }
        }
    }

    public void checkOut() {
        if(loggedIn) {
            try {
                if (patient.isDone == 0) {
                    myRef.child(patientString).child("isDone").setValue(1);
                    myRef.child(patientString).child("end24").setValue(getTime());
                }
            }
            catch (Exception e) {
                Log.d("TimeDebug", e.toString());
            }
        }
    }

    public static Long getTime() {
        Date currentTime = Calendar.getInstance().getTime();
        String time = currentTime.toString().split(" ")[3].split(":")[0] + currentTime.toString().split(" ")[3].split(":")[1];
        Long ltime = Long.valueOf(time);
        return ltime;
    }


    public static Long addThirtyMinutes(Long ihatemylife) {
        //WHY THE FREAK ARE WE REPRESENTING TIME WITH LONGS
        String s = String.valueOf(ihatemylife);
        int b = Integer.valueOf(s.substring(0,2));
        int e = Integer.valueOf(s.substring(2, 4));
        e = e + 30;
        if (e>=60) {
            e = e-60;
            b = b + 1;
            if(b==25) {
                b = 0;
            }
        }
        String bb = String.valueOf(b);
        String ee = String.valueOf(e);
        while(bb.length() < 2) {
            bb = 0 + bb;
        }
        while(ee.length() < 2) {
            ee = 0 + ee;
        }
        return Long.valueOf(bb + ee);

    }


}
