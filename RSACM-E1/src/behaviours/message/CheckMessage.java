package behaviours.message;

public class CheckMessage {
    private String relationType;
    private String checkMode;
    private int period;
    private int requirementID;
    private int processID;
    private String failedAgentName;
    private String resourceType;
    private int serviceNum;
    private int noiseRate;

    public int getNoiseRate() {
        return noiseRate;
    }

    public void setNoiseRate(int noiseRate) {
        this.noiseRate = noiseRate;
    }

    public int getProcessID() {
        return processID;
    }

    public void setProcessID(int processID) {
        this.processID = processID;
    }

    public int getRequirementID() {
        return requirementID;
    }

    public void setRequirementID(int requirementID) {
        this.requirementID = requirementID;
    }

    public int getServiceNum() {
        return serviceNum;
    }

    public void setServiceNum(int serviceNum) {
        this.serviceNum = serviceNum;
    }

    public String getResourceType() {
        return resourceType;
    }

    public void setResourceType(String resourceType) {
        this.resourceType = resourceType;
    }

    public String getRelationType() {
        return relationType;
    }

    public void setRelationType(String relationType) {
        this.relationType = relationType;
    }

    public String getCheckMode() {
        return checkMode;
    }

    public void setCheckMode(String checkMode) {
        this.checkMode = checkMode;
    }

    public int getPeriod() {
        return period;
    }

    public void setPeriod(int period) {
        this.period = period;
    }

    public String getFailedAgentName() {
        return failedAgentName;
    }

    public void setFailedAgentName(String failedAgentName) {
        this.failedAgentName = failedAgentName;
    }
}
