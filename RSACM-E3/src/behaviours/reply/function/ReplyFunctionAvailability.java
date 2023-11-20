package behaviours.reply.function;

import behaviours.gather.GatherAvailableReply;
import behaviours.message.AvailableMessage;
import behaviours.message.CheckMessage;
import behaviours.reply.GeneralCyclicService;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import functionAgents.AgentAttributes;
import jade.core.AID;
import jade.domain.FIPAException;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import util.JadeUtil;
import util.Tuple;

import java.io.IOException;
import java.util.*;

import static behaviours.gather.GatherCheckReply.append2file;

public class ReplyFunctionAvailability extends GeneralCyclicService {
    //    public ReceiveAvailableQuest(AID[] combFunction, AID[] aggFunction, AID[] depFunction, AID[] repFunction, AID[] resources, Deque<String> aggQueue, StringBuilder selectedAgg, AtomicInteger serviceNum) {
//        super(combFunction, aggFunction, depFunction, repFunction, resources, aggQueue, selectedAgg, serviceNum);
//    }
//    public static Map<String, ArrayList<String>> replacementMap = null;
//    public static Map<String, ArrayList<String>> replacementMap;

    public ReplyFunctionAvailability(AgentAttributes agentAttributes) {
        super(agentAttributes);
//        this.replacementMap = replacementMap;
//        replacementMap = agentAttributes.replacementMap;
    }


//    private Boolean requireSuccess = false;

    ObjectMapper mapper = new ObjectMapper();
    //    private int requiredNum;
    int step = 0;

    @Override
    public void action() {

        MessageTemplate mt = MessageTemplate.and(MessageTemplate.MatchPerformative(ACLMessage.REQUEST),
                                                 MessageTemplate.MatchConversationId("ask-capacity-available"));

        ACLMessage askAvailableMsg = myAgent.receive(mt);
        if (askAvailableMsg != null) {
            String myAgentName = JadeUtil.getAgentName(myAgent.getAID());


            AvailableMessage availableMessage;
            try {
                availableMessage = mapper.readValue(askAvailableMsg.getContent(),
                                                    AvailableMessage.class);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            ACLMessage reply = new ACLMessage(ACLMessage.INFORM);
            reply.setConversationId("answer-capacity-available");
            int requiredNum = availableMessage.getRequiredNum();
            String qos = availableMessage.getRequiredType();
            int urgencyLevel = availableMessage.getUrgencyLevel();
            int period = availableMessage.getPeriod();
            String rqId = availableMessage.getRequirementID();
            String relationType = availableMessage.getRelationType();
            AvailableMessage replyContent = new AvailableMessage();

            if (availableFlag.get() == true) {
                replyContent.setType("beAsked");
                try {
                    reply.setContent(mapper.writeValueAsString(replyContent));
                    reply.addReceiver(askAvailableMsg.getSender());
                    myAgent.send(reply);
                } catch (JsonProcessingException e) {
                    throw new RuntimeException(e);
                }
            } else {
                availableFlag.set(true);
                String dir = JadeUtil.outputPath;
                String fileName1 = "功能agent容量-错误.txt";
                append2file(dir + fileName1,
                            rqId + ":" +myAgentName+","+serviceNum.get() + "\n");
                try {
                    int MsgNum = sendAvailableMsg2Nei(availableMessage,
                                                      askAvailableMsg.getSender().getLocalName());
                    myAgent.addBehaviour(
                            new GatherAvailableReply(MsgNum, requiredNum, askAvailableMsg));

                } catch (JsonProcessingException e) {
                    throw new RuntimeException(e);
                }
//                if (requiredNum > serviceNum.get()) {
//                    //这里添加替换模块
//                    Tuple<Boolean, HashMap<String, Set<String>>> tuple = checkPossible2Replace();
//                    if (tuple.a == true && urgencyLevel >= 3) {
//                        int sendNum = 0;
//                        try {
//                            sendNum = sendCheckMsg2Rep(tuple.b);
//                        } catch (JsonProcessingException e) {
//                            throw new RuntimeException(e);
//                        }
//                        myAgent.addBehaviour(new GatherReplaceReply(sendNum, tuple.b, askAvailableMsg,
//                                                                    new Map[]{highQualityRes, lowCostRes}, selectedAgg,
//                                                                    availableNei, serviceNum));
//                    } else {
//                        try {
//                            int MsgNum = sendAvailableMsg2Nei(availableMessage,
//                                                              askAvailableMsg.getSender().getLocalName());
//                            if (MsgNum != -1) {
//                                myAgent.addBehaviour(
//                                        new GatherAvailableReply(MsgNum, requiredNum, askAvailableMsg));
//                            } else {
//                                replyContent.setType("fail");
//                                replyContent.setHitResNum(0);
//                                System.out.println(myAgentName + "匹配资源失败");
//                                try {
//                                    reply.setContent(mapper.writeValueAsString(replyContent));
//                                } catch (JsonProcessingException e) {
//                                    throw new RuntimeException(e);
//                                }
//                                reply.addReceiver(askAvailableMsg.getSender());
//                                myAgent.send(reply);
//                            }
//                        } catch (JsonProcessingException e) {
//                            throw new RuntimeException(e);
//                        }
//
////                        replyContent.setType("fail");
////                        replyContent.setRelationType(relationType);
////                        replyContent.setHitResNum(0);
////                        System.out.println(myAgentName + "容量不足，无法提供服务");
////                        try {
////                            reply.setContent(mapper.writeValueAsString(replyContent));
////                        } catch (JsonProcessingException e) {
////                            throw new RuntimeException(e);
////                        }
////                        reply.addReceiver(askAvailableMsg.getSender());
////                        myAgent.send(reply);
//                    }
//
//                } else {
////                    requireSuccess = true;
//                    System.out.println("[请求]" + JadeUtil.getDateTime() + ":" + myAgentName + "容量足够，正在询问邻居容量");
//                    try {
//                        int MsgNum = sendAvailableMsg2Nei(availableMessage,
//                                                          askAvailableMsg.getSender().getLocalName());
//                        if (MsgNum != -1) {
//                            myAgent.addBehaviour(
//                                    new GatherAvailableReply(MsgNum, requiredNum, askAvailableMsg));
//                        } else {
//                            replyContent.setType("fail");
//                            replyContent.setHitResNum(0);
//                            System.out.println(myAgentName + "匹配资源失败");
//                            try {
//                                reply.setContent(mapper.writeValueAsString(replyContent));
//                            } catch (JsonProcessingException e) {
//                                throw new RuntimeException(e);
//                            }
//                            reply.addReceiver(askAvailableMsg.getSender());
//                            myAgent.send(reply);
//                        }
//
//                    } catch (JsonProcessingException e) {
//                        throw new RuntimeException(e);
//                    }
//                }
            }
        } else {
            block();
        }


    }

    private int sendAvailableMsg2Nei(AvailableMessage requestMessage, String asker) throws JsonProcessingException {
        int sendNum = 0;
        ACLMessage askAvailAnd = new ACLMessage(ACLMessage.REQUEST);
        ACLMessage askAvailOr = new ACLMessage(ACLMessage.REQUEST);
        ACLMessage askAvailAdd = new ACLMessage(ACLMessage.REQUEST);
//        ACLMessage askAvailableMsg = new ACLMessage(ACLMessage.REQUEST);
        sendNum += addNei2Receivers(combFunction, asker, askAvailAnd);
        sendNum += addNei2Receivers(depFunction, asker, askAvailAnd);
//        sendNum += addNei2Receivers(resources, asker, askAvailableMsg);
        String rqID = requestMessage.getRequirementID();
        String qos = requestMessage.getRequiredType();
        int UrgencyLevel = requestMessage.getUrgencyLevel();
        int requireNum = requestMessage.getRequiredNum();
        int period = requestMessage.getPeriod();
        if (sendNum != 0) {
            AvailableMessage askContent = new AvailableMessage();
            askContent.setRelationType("and");
            askContent.setRequirementID(rqID);
            askContent.setPeriod(period);
            askContent.setRequiredType(qos);
            askContent.setUrgencyLevel(UrgencyLevel);
            askContent.setRequiredNum(requireNum);
            askAvailAnd.setConversationId("ask-capacity-available");
            askAvailAnd.setContent(mapper.writeValueAsString(askContent));
            myAgent.send(askAvailAnd);
        }
        if (aggFunction!=null&&aggFunction.size()!=0) {
            AvailableMessage askContent = new AvailableMessage();
            askContent.setRelationType("or");
            askContent.setRequirementID(rqID);
            askContent.setPeriod(period);
            askContent.setRequiredType(qos);
            askContent.setUrgencyLevel(UrgencyLevel);
            askContent.setRequiredNum(requireNum);
//            Map.Entry<String, Integer> selectedAggAgent = selectedAgg.entrySet().iterator().next();
//            String selectedAggName = selectedAggAgent.getKey();
            AID selectedAggAID = aggFunction.get(0);
//            selectedAggAID.setName(selectedAggName);
            askAvailOr.addReceiver(selectedAggAID);
            askAvailOr.setConversationId("ask-capacity-available");
            askAvailOr.setContent(mapper.writeValueAsString(askContent));
            sendNum++;
            myAgent.send(askAvailOr);
        }
        String requireType = requestMessage.getRequiredType();
        String mAgentName = myAgent.getLocalName();
        if (resources != null && resources.size() != 0) {
            String rString = rqID+"-"+myAgent.getLocalName()+"-"+qos+"-"+UrgencyLevel;
            int rSeed=JadeUtil.convertString2Int(rString);
            int index = new Random(rSeed).nextInt(resources.size());
            askAvailAdd.addReceiver(resources.get(index));
            AvailableMessage askContent = new AvailableMessage();
            askContent.setRelationType("add");
            askContent.setRequirementID(rqID);
            askContent.setPeriod(period);
            askContent.setRequiredType(qos);
            askContent.setUrgencyLevel(UrgencyLevel);
            askContent.setRequiredNum(requireNum);
            askAvailAdd.setConversationId("ask-capacity-available");
            askAvailAdd.setContent(mapper.writeValueAsString(askContent));
            myAgent.send(askAvailAdd);
            sendNum++;
        }
        return sendNum;
    }

    public Set<String> findRepFunctions(String failedFun) throws FIPAException {
        Set<String> repFunctions = new HashSet<>();
        if (replaceView.containsKey(failedFun)) {
            Set<String> functions = replaceView.get(failedFun);
            for (String repFun : functions) {
                if (JadeUtil.search_agent_exist(myAgent, repFun)) {
                    repFunctions.add(repFun);
                }
            }
        }
        return repFunctions;
    }

    public int sendCheckMsg2Rep(HashMap<String, Set<String>> RepFunctions) throws JsonProcessingException {
        int cnt = 0;
        for (Map.Entry<String, Set<String>> entry : RepFunctions.entrySet()) {
            ACLMessage checkStatusMsg = new ACLMessage(ACLMessage.REQUEST);
            checkStatusMsg.setConversationId("check-capacity");
            String failedName = entry.getKey();
            Set<String> reps = entry.getValue();
            for (String rep : reps) {
                AID repAID = new AID(rep, AID.ISLOCALNAME);
                checkStatusMsg.addReceiver(repAID);
                cnt++;
                CheckMessage checkMessage = new CheckMessage();
                checkMessage.setRelationType("None");
                checkMessage.setCheckMode("replaceMode");
                checkMessage.setFailedAgentName(failedName);
                checkStatusMsg.setContent(mapper.writeValueAsString(checkMessage));
            }
            myAgent.send(checkStatusMsg);
        }
        return cnt;
    }


    public Tuple<Boolean, HashMap<String, Set<String>>> checkPossible2Replace() {
        boolean possibleReplace = true;
        HashMap<String, Set<String>> rs = new HashMap<>();
        for (String failedFun : failedNei) {
//            System.out.println("here" + replaceView);
            if (replaceView.containsKey(failedFun)) {
                System.out.println("[替换视图]" + failedFun + "的替换为："
                                           + replaceView.get(failedFun));
                try {
                    Set<String> repFunctions = findRepFunctions(failedFun);
                    if (repFunctions != null && repFunctions.size() != 0) {
                        rs.put(failedFun, repFunctions);
                    } else {
                        possibleReplace = false;
                        break;
                    }
                } catch (FIPAException e) {
                    throw new RuntimeException(e);
                }
            } else {
                possibleReplace = false;
                break;
            }
        }
        return new Tuple<>(possibleReplace, rs);
    }
}
