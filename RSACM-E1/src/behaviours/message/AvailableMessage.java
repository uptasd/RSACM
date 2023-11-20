package behaviours.message;

import java.util.Map;

public class AvailableMessage {
    private String type = null; //fail or success
    private Map<String, Integer> requiredAgent = null;
    private String replaceAgent = null;
    private int requiredNum = 0;
    private String requiredType = null; //high-quality or low-cost
    private int urgencyLevel;
    private int period;

    public int getPeriod() {
        return period;
    }

    public void setPeriod(int period) {
        this.period = period;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public Map<String, Integer> getRequiredAgent() {
        return requiredAgent;
    }

    public void setRequiredAgent(Map<String, Integer> requiredAgent) {
        this.requiredAgent = requiredAgent;
    }

    public String getReplaceAgent() {
        return replaceAgent;
    }

    public void setReplaceAgent(String replaceAgent) {
        this.replaceAgent = replaceAgent;
    }

    public int getRequiredNum() {
        return requiredNum;
    }

    public void setRequiredNum(int requiredNum) {
        this.requiredNum = requiredNum;
    }

    public String getRequiredType() {
        return requiredType;
    }

    public void setRequiredType(String requiredType) {
        this.requiredType = requiredType;
    }

    public int getUrgencyLevel() {
        return urgencyLevel;
    }

    public void setUrgencyLevel(int urgencyLevel) {
        this.urgencyLevel = urgencyLevel;
    }
}
