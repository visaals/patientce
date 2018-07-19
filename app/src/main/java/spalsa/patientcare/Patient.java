package spalsa.patientcare;

public class Patient {

    public long CheckedIn;
    public long Start24;
    public long End24;
    public long SchedStart24;
    public long SchedEnd24;

    public Patient() {

    }

    public String toString() {
        return "Checkedin: " + CheckedIn + "\nStart24: " + Start24 + "\nEnd24: " + End24 + "\nSchedStart24: " + SchedStart24 + "\nSchedEnd24: " + SchedEnd24;
    }

    public long delay() {
        return Start24 - SchedStart24;
    }

    public static String longToString(long l) {
        String s =  String.valueOf(l);
        while (s.length() < 4) {
            s = "0" + s;
        }
        return s;
    }

    public String stringSchedStart24() {
        return longToString(SchedStart24);
    }

    public String stringSchedEnd24() {
        return longToString(SchedStart24);
    }

    public String stringStar24() {
        return longToString(SchedStart24);
    }
    public String stringEnd24() {
        return longToString(SchedStart24);
    }

}
