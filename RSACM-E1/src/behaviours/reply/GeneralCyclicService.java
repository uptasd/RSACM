package behaviours.reply;

import functionAgents.AgentAttributes;
import jade.core.AID;
import jade.core.behaviours.CyclicBehaviour;
import jade.lang.acl.ACLMessage;

import java.util.ArrayList;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

public class GeneralCyclicService extends CyclicBehaviour {
    public ArrayList<AID> combFunction;
    public ArrayList<AID> aggFunction;
    public ArrayList<AID> depFunction;
    public ArrayList<AID> repFunction;
    public ArrayList<AID> resources;
    public Map<String, Integer> selectedAgg;
    public Map<StringBuilder, Integer> highQualityRep;
    public Map<StringBuilder, Integer> lowCostRep;
    public Map<String, Integer> highQualityRes;
    public Map<String, Integer> lowCostRes;
    public String resourceType;
    //    Deque<String> aggQueue;
    public AtomicInteger serviceNum;
    public AtomicInteger neededNum;
    public AtomicInteger unavailableNum;
    public StringBuilder updateFlag;
    //    public int[] aggProbability;
//    public Boolean isResource;
//    public AtomicBoolean decreasedFlag;
//    public AtomicBoolean increaseFlag;
    public AtomicBoolean availableFlag;
    //    public AtomicBoolean latestFlag;
    public int serviceFactor;
    //    public Deque<List<String>> offerDeque;
    public ArrayList<String> failedNei;
    public ArrayList<String> availableNei;
    public static Map<String, Set<String>> replaceView;
    public static Map<String, ArrayList<String>> replacementMap;
    public static Map<String, Integer> updatedFunctions;
    public String working_time;
    public AtomicInteger recoveryNum;
    public Map<Integer, Integer> periodStatus;

    public GeneralCyclicService(AgentAttributes agentAttributes) {
        this.combFunction = agentAttributes.combFunction;
        this.aggFunction = agentAttributes.aggFunction;
        this.depFunction = agentAttributes.depFunction;
        this.repFunction = agentAttributes.repFunction;
        this.selectedAgg = agentAttributes.selectedAgg;
        this.serviceNum = agentAttributes.serviceNum;

        this.resources = agentAttributes.resources;

        this.availableFlag = agentAttributes.availableFlag;

        this.lowCostRep = agentAttributes.lowCostRep;
        this.highQualityRep = agentAttributes.highQualityRep;
        this.unavailableNum = agentAttributes.unavailableNum;
        this.resourceType = agentAttributes.resourceType;
        this.highQualityRes = agentAttributes.highQualityRes;
        this.lowCostRes = agentAttributes.lowCostRes;
        this.updateFlag = agentAttributes.updateFlag;
        this.failedNei = agentAttributes.failedNei;
        this.availableNei = agentAttributes.availableNei;
        this.replaceView = agentAttributes.replaceView;
        this.replacementMap = agentAttributes.replacementMap;
        this.updatedFunctions = agentAttributes.updatedFunctions;
        this.working_time = agentAttributes.working_time;
        this.recoveryNum = agentAttributes.recoveryNum;
        this.periodStatus = agentAttributes.periodStatus;
    }

    @Override
    public void action() {

    }

//    @Deprecated
//    public void sendUpdateMsg2Nei(String updateType, int Num) {
//        //增加或减少容量
////        System.out.println("----正在" + updateType + "子功能容量-----");
//        String agentName = JadeUtil.getAgentName(myAgent.getAID());
//        ACLMessage inform;
//        if (updateType == "减少") {
//            inform = new ACLMessage(ACLMessage.CFP);
//        } else {
//            inform = new ACLMessage(ACLMessage.INFORM);
//        }
//        List<String> NeiAgent;
//        if (updateType.equals("减少")) {
//            NeiAgent = offerDeque.getFirst();
//            for (String NeiName : NeiAgent) {
//                AID a = new AID();
//                a.setName(NeiName);
//                inform.addReceiver(a);
//            }
//        } else {
//
//        }
////        addNei2Receivers(combFunction, "组合", inform, updateType);
////        addNei2Receivers(depFunction, "依赖", inform, updateType);
////        addNei2Receivers(resources, "资源", inform, updateType);
//
//        if (aggFunction != null) {
////            System.out.println("here");
//            AID targetAgent = new AID();
//            if (updateType.equals("减少")) {
//                targetAgent.setName(selectedAgg.toString());
//                aggQueue.addLast(selectedAgg.toString());
//                System.out.println(agentName + "的聚合功能占用队列为:" + aggQueue);
//            } else if (updateType.equals("增加")) {
//                targetAgent.setName(aggQueue.removeFirst());
//            }
//            System.out.println(JadeUtil.getDateTime() + "：通知" + agentName + "的聚合功能-" + JadeUtil.getAgentName(
//                    targetAgent) + updateType + "容量");
//            inform.addReceiver(targetAgent);
//            System.out.println(targetAgent.getName());
//        }
//
//        inform.setContent(String.valueOf(Num));
//        String ConversationId = "";
//        if (updateType.equals("减少")) {
//            ConversationId = "decrease-capacity";
//        } else if (updateType.equals("增加")) {
//            ConversationId = "increase-capacity";
//        }
//        inform.setConversationId(ConversationId);
//        inform.setReplyWith("INFORM" + System.currentTimeMillis());
//        myAgent.send(inform);
//    }


    public int addNei2Receivers(ArrayList<AID> Functions, String askerName, ACLMessage inform) {
        int sendNum = 0;
        if (Functions != null) {
            for (int i = 0; i < Functions.size(); i++) {
                if (!Functions.get(i).getName().equals(askerName)) {
//                    System.out.println(Functions[i]);
                    inform.addReceiver(Functions.get(i));
                }
                sendNum++;
            }
        }
        return sendNum;
    }


}

