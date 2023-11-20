package util;

import jade.core.AID;

public class RequirementInfo {
    AID requiredFunction;
    Float requiredTime;
    String requireQos;
    Integer urgencyLevel;

    public AID getRequiredFunction() {
        return requiredFunction;
    }

    public void setRequiredFunction(AID requiredFunction) {
        this.requiredFunction = requiredFunction;
    }

    public Float getRequiredTime() {
        return requiredTime;
    }

    public void setRequiredTime(Float requiredTime) {
        this.requiredTime = requiredTime;
    }

    public String getRequireQos() {
        return requireQos;
    }

    public void setRequireQos(String requireQos) {
        this.requireQos = requireQos;
    }

    public Integer getUrgencyLevel() {
        return urgencyLevel;
    }

    public void setUrgencyLevel(Integer urgencyLevel) {
        this.urgencyLevel = urgencyLevel;
    }
}
