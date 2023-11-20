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
    private String requirementID;
    private int hitResNum;
    private String relationType;

    public String getRequirementID() {
        return requirementID;
    }

    public void setRequirementID(String requirementID) {
        this.requirementID = requirementID;
    }

    public String getRelationType() {
        return relationType;
    }

    public void setRelationType(String relationType) {
        this.relationType = relationType;
    }

    public int getHitResNum() {
        return hitResNum;
    }

    public void setHitResNum(int hitResNum) {
        this.hitResNum = hitResNum;
    }

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
