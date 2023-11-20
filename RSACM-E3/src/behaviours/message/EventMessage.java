package behaviours.message;

public class EventMessage {
    private int noiseRate;
    private int affectedNum;
    private String affectedAgent;
    private boolean affectedFlag;
    private int period;

    public boolean isAffectedFlag() {
        return affectedFlag;
    }

    public void setAffectedFlag(boolean affectedFlag) {
        this.affectedFlag = affectedFlag;
    }

    public int getNoiseRate() {
        return noiseRate;
    }

    public void setNoiseRate(int noiseRate) {
        this.noiseRate = noiseRate;
    }

    public String getAffectedAgent() {
        return affectedAgent;
    }

    public void setAffectedAgent(String affectedAgent) {
        this.affectedAgent = affectedAgent;
    }

    public int getAffectedNum() {
        return affectedNum;
    }

    public void setAffectedNum(int affectedNum) {
        this.affectedNum = affectedNum;
    }

    public int getPeriod() {
        return period;
    }

    public void setPeriod(int period) {
        this.period = period;
    }
}
