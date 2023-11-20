package util;

import java.io.Serializable;

public class Tuple <T1 extends Serializable, T2 extends Serializable>{
    public final T1 a;
    public final T2 b;

    public Tuple(T1 a, T2 b) {
        this.a = a;
        this.b = b;
    }

}
