package behaviours.message;

public class DecreaseMessage {
    String type;
    Integer requiredNum;
    Integer decreasedNum;

    public Integer getDecreasedNum() {
        return decreasedNum;
    }

    public void setDecreasedNum(Integer decreasedNum) {
        this.decreasedNum = decreasedNum;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public Integer getRequiredNum() {
        return requiredNum;
    }

    public void setRequiredNum(Integer requiredNum) {
        this.requiredNum = requiredNum;
    }
}
