package functionAgents;

import jade.core.AID;

import java.util.ArrayList;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

public class AgentAttributes {
    public ArrayList<AID> combFunction = null;
    public ArrayList<AID> aggFunction = null;
    public ArrayList<AID> depFunction = null;
    public ArrayList<AID> repFunction = null;
    public ArrayList<AID> resources = null;
    public Map<String, Integer> selectedAgg = null;
    public Map<StringBuilder, Integer> highQualityRep = null;
    public Map<StringBuilder, Integer> lowCostRep = null;
    public Map<String, Integer> highQualityRes = null;
    public Map<String, Integer> lowCostRes = null;
    public String resourceType = null;
    //    public Deque<String> aggQueue = null;
//    public Deque<List<String>> offerDeque = null;
    public AtomicInteger serviceNum = null;
    //    public AtomicInteger neededNum = null;
    public StringBuilder updateFlag = null;

    //    public int[] aggProbability = null;
    public Boolean isResource = null;
    //    public AtomicBoolean decreasedFlag = null;
//    public AtomicBoolean increaseFlag = null;
    public AtomicBoolean availableFlag = null;
    //    public AtomicBoolean latestFlag = null;
    public AtomicInteger unavailableNum = null;
    //    public Map<String, ArrayList<String>> replacementMap = null;
    public ArrayList<String> failedNei = new ArrayList<>();
    public ArrayList<String> availableNei = new ArrayList<>();
    public static Map<String, Set<String>> replaceView = null;
    public static Map<String, ArrayList<String>> replacementMap;
    public static Map<String, Integer> updatedFunctions;
    public String working_time;
    public AtomicInteger recoveryNum ;
    public Map<Integer, Integer> periodStatus;
    public AtomicInteger last_serviceNum;

    //    public int serviceFactor = 1;
//    public AgentAttributes replacementMap(Map<String, ArrayList<String>> replacementMap) {
//        this.replacementMap = replacementMap;
//        return this;
//    }
    public AgentAttributes periodStatus(Map<Integer, Integer> periodStatus) {
        this.periodStatus = periodStatus;
        return this;
    }
    public AgentAttributes last_serviceNum(AtomicInteger last_serviceNum) {
        this.last_serviceNum = last_serviceNum;
        return this;
    }
    public AgentAttributes recoveryNum(AtomicInteger recoveryNum) {
        this.recoveryNum = recoveryNum;
        return this;
    }
    public AgentAttributes working_time(String working_time) {
        this.working_time = working_time;
        return this;
    }
    public AgentAttributes updatedFunctions(Map<String, Integer> updatedFunctions) {
        this.updatedFunctions = updatedFunctions;
        return this;
    }
    public AgentAttributes replaceView(Map<String, Set<String>> replaceView) {
        this.replaceView = replaceView;
        return this;
    }
    public AgentAttributes replacementMap(Map<String, ArrayList<String>> replacementMap) {
        this.replacementMap = replacementMap;
        return this;
    }

    public AgentAttributes failedNei(ArrayList<String> failedNei) {
        this.failedNei = failedNei;
        return this;
    }

    public AgentAttributes availableNei(ArrayList<String> availableNei) {
        this.availableNei = availableNei;
        return this;
    }

    public AgentAttributes combFunction(ArrayList<AID> combFunction) {
        this.combFunction = combFunction;
        return this;
    }

    public AgentAttributes aggFunction(ArrayList<AID> aggFunction) {
        this.aggFunction = aggFunction;
        return this;
    }

    public AgentAttributes depFunction(ArrayList<AID> depFunction) {
        this.depFunction = depFunction;
        return this;
    }

    public AgentAttributes repFunction(ArrayList<AID> repFunction) {
        this.repFunction = repFunction;
        return this;
    }

    public AgentAttributes resources(ArrayList<AID> resources) {
        this.resources = resources;
        return this;
    }

    public AgentAttributes selectedAgg(Map<String, Integer> selectedAgg) {
        this.selectedAgg = selectedAgg;
        return this;
    }

    public AgentAttributes highQualityRep(Map<StringBuilder, Integer> highQualityRep) {
        this.highQualityRep = highQualityRep;
        return this;
    }

    public AgentAttributes lowCostRep(Map<StringBuilder, Integer> lowCostRep) {
        this.lowCostRep = lowCostRep;
        return this;
    }

//    public AgentAttributes aggQueue(Deque<String> aggQueue) {
//        this.aggQueue = aggQueue;
//        return this;
//    }

    public AgentAttributes serviceNum(AtomicInteger serviceNum) {
        this.serviceNum = serviceNum;
        return this;
    }

//    public AgentAttributes neededNum(AtomicInteger neededNum) {
//        this.neededNum = neededNum;
//        return this;
//    }

//    public AgentAttributes aggProbability(int[] aggProbability) {
//        this.aggProbability = aggProbability;
//        return this;
//    }

//    public AgentAttributes isResource(Boolean isResource) {
//        this.isResource = isResource;
//        return this;
//    }

//    public AgentAttributes decreasedFlag(AtomicBoolean decreasedFlag) {
//        this.decreasedFlag = decreasedFlag;
//        return this;
//    }

//    public AgentAttributes increaseFlag(AtomicBoolean increaseFlag) {
//        this.increaseFlag = increaseFlag;
//        return this;
//    }

    public AgentAttributes availableFlag(AtomicBoolean availableFlag) {
        this.availableFlag = availableFlag;
        return this;
    }

//    public AgentAttributes latestFlag(AtomicBoolean latestFlag) {
//        this.latestFlag = latestFlag;
//        return this;
//    }

//    public AgentAttributes serviceFactor(int serviceFactor) {
//        this.serviceFactor = serviceFactor;
//        return this;
//    }

//    public AgentAttributes offerDeque(Deque<List<String>> offerDeque) {
//        this.offerDeque = offerDeque;
//        return this;
//    }

    public AgentAttributes updateFlag(StringBuilder updateFlag) {
        this.updateFlag = updateFlag;
        return this;
    }

    public AgentAttributes unavailableNum(AtomicInteger unavailableNum) {
        this.unavailableNum = unavailableNum;
        return this;
    }

    public AgentAttributes highQualityRes(Map<String, Integer> highQualityRes) {
        this.highQualityRes = highQualityRes;
        return this;
    }

    public AgentAttributes lowCostRes(Map<String, Integer> lowCostRes) {
        this.lowCostRes = lowCostRes;
        return this;
    }

    public AgentAttributes resourceType(String resourceType) {
        this.resourceType = resourceType;
        return this;
    }
}
