package spalsa.patientcare;

public class Patient {

    public long isCheckedIn;
    public long isCancelled;
    public long start24;
    public long end24;
    public long schedStart24;
    public long schedEnd24;
    public long isDone;

    public Patient() {

    }

    public String toString() {
        return "isCheckedIn: " + isCheckedIn + "isCancelled: " + isCancelled + "\nStart24: " + start24 + "\nEnd24: " + end24 + "\nSchedStart24: " + schedStart24 + "\nSchedEnd24: " + schedEnd24;
    }

    public long delay() {
        return start24 - schedStart24;
    }

    public static String longToString(long l) {
        String s =  String.valueOf(l);
        while (s.length() < 4) {
            s = "0" + s;
        }
        s = s.substring(0,2) + ":" + s.substring(2,4);
        return s;
    }

    public String stringSchedStart24() {
        return longToString(schedStart24);
    }

    public String stringSchedEnd24() {
        return longToString(schedStart24);
    }

    public String stringStar24() {
        return longToString(schedStart24);
    }
    public String stringEnd24() {
        return longToString(schedStart24);
    }

}
