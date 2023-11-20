package behaviours.reply.function;

import behaviours.gather.GatherCheckReply;
import behaviours.message.CheckMessage;
import behaviours.reply.GeneralCyclicService;
import com.fasterxml.jackson.databind.ObjectMapper;
import functionAgents.AgentAttributes;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;

import java.io.IOException;
import java.util.Map;

public class ReplyFunctionStatus extends GeneralCyclicService {

    private String askerName;

    public ReplyFunctionStatus(AgentAttributes agentAttributes) {
        super(agentAttributes);
    }

    //    private ACLMessage replyMsg;

    @Override
    public void action() {
//        System.out.println("here");
        MessageTemplate checkMT = MessageTemplate.and(MessageTemplate.MatchPerformative(ACLMessage.REQUEST),
                                                      MessageTemplate.MatchConversationId("check-capacity"));
        ACLMessage checkMsg = myAgent.receive(checkMT);
        if (checkMsg != null) {

            String mAgentName = myAgent.getLocalName();
//            if (mAgentName.equals("脊柱侧弯中心-医生值班")) {
//                System.out.println(replaceView);
//
//            }
            ObjectMapper mapper = new ObjectMapper();
            CheckMessage checkMessage = null;
            try {
                checkMessage = mapper.readValue(checkMsg.getContent(), CheckMessage.class);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            int period = checkMessage.getPeriod();
            int requirementID = checkMessage.getRequirementID();
            int processID = checkMessage.getProcessID();
            int noiseRate= checkMessage.getNoiseRate();
//            if (mAgentName.equals("脊柱侧弯中心-医生值班") && period == 2) {
//                System.out.println(askerName);
//            }
            if (updatedFunctions.containsKey(mAgentName)) {
                String checkID=period+"-"+requirementID+"-"+processID;
                myAgent.addBehaviour(new GatherCheckReply(serviceNum, checkMsg, true, checkID));
            } else {
                updatedFunctions.put(mAgentName, 0);
                askerName = checkMsg.getSender().getLocalName();
                availableFlag.set(false);
                int[] num;
                try {
                    num = sendCheckMsg2Neighbors(checkMsg);
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }

                highQualityRes.clear();
                lowCostRes.clear();
                selectedAgg.clear();
                failedNei.clear();
                availableNei.clear();
                //添加收集器
                myAgent.addBehaviour(new GatherCheckReply(num, serviceNum, checkMsg, selectedAgg,
                                                          new Map[]{highQualityRep, lowCostRep}, repFunction,
                                                          new Map[]{highQualityRes, lowCostRes}, failedNei,
                                                          availableNei, replaceView, replacementMap, updatedFunctions,
                                                          last_serviceNum,noiseRate));
            }

        } else {
            block();
        }
    }


    public int[] sendCheckMsg2Neighbors(ACLMessage checkMsg) throws IOException {
        int andRepliesNum = 0;
        int orRepliesNum = 0;
        int addRepliesNum = 0;
//        int replaceRepliesNum = 0;
        ACLMessage askCapacityAnd = new ACLMessage(ACLMessage.REQUEST);
        ACLMessage askCapacityOr = new ACLMessage(ACLMessage.REQUEST);
        ACLMessage askCapacityAdd = new ACLMessage(ACLMessage.REQUEST);
//        ACLMessage askCapacityReplace = new ACLMessage(ACLMessage.REQUEST);
        //询问邻居的状态
        andRepliesNum += addNei2Receivers(combFunction, askerName, askCapacityAnd);
        andRepliesNum += addNei2Receivers(depFunction, askerName, askCapacityAnd);
        addRepliesNum += addNei2Receivers(resources, askerName, askCapacityAdd);
        orRepliesNum += addNei2Receivers(aggFunction, askerName, askCapacityOr);
//        replaceRepliesNum += addNei2Receivers(repFunction, askerName, askCapacityReplace, "检查");
        ObjectMapper mapper = new ObjectMapper();
        CheckMessage requireCheckMsg = mapper.readValue(checkMsg.getContent(), CheckMessage.class);
        String askerCheckMode = requireCheckMsg.getCheckMode();
        int period = requireCheckMsg.getPeriod();
        int noiseRate = requireCheckMsg.getNoiseRate();
        String checkMode = "normal";
        if (askerCheckMode.equals("replaceMode") || askerCheckMode.equals("normal")) {
            checkMode = "normal";
        } else if (askerCheckMode.equals("global")) {
            checkMode = "global";
        }

        if (andRepliesNum != 0) {
            askCapacityAnd.setConversationId("check-capacity");
            askCapacityAnd.setReplyWith("REQUEST" + System.currentTimeMillis());
//            System.out.println("here"+checkMsg.getContent());
            CheckMessage checkMessage = new CheckMessage();
            checkMessage.setRelationType("and");
            checkMessage.setCheckMode(checkMode);
            checkMessage.setPeriod(period);
            checkMessage.setNoiseRate(noiseRate);
            askCapacityAnd.setContent(mapper.writeValueAsString(checkMessage));
            myAgent.send(askCapacityAnd);
//            askCapacityAnd.clearAllReceiver();
        }
        if (orRepliesNum != 0) {
            askCapacityOr.setConversationId("check-capacity");
            askCapacityOr.setReplyWith("REQUEST" + System.currentTimeMillis());
            CheckMessage checkMessage = new CheckMessage();
            checkMessage.setRelationType("or");
            checkMessage.setCheckMode(checkMode);
            checkMessage.setPeriod(period);
            checkMessage.setNoiseRate(noiseRate);
            askCapacityOr.setContent(mapper.writeValueAsString(checkMessage));
            myAgent.send(askCapacityOr);
//            askCapacityOr.clearAllReceiver();
        }
        if (addRepliesNum != 0) {
            askCapacityAdd.setConversationId("check-capacity");
            askCapacityAdd.setReplyWith("REQUEST" + System.currentTimeMillis());
            CheckMessage checkMessage = new CheckMessage();
            checkMessage.setRelationType("add");
            checkMessage.setCheckMode(checkMode);
            checkMessage.setPeriod(period);
            checkMessage.setNoiseRate(noiseRate);
            askCapacityAdd.setContent(mapper.writeValueAsString(checkMessage));
            myAgent.send(askCapacityAdd);
//            askCapacityOr.clearAllReceiver();
        }
        return new int[]{andRepliesNum, orRepliesNum, addRepliesNum};
    }

}
