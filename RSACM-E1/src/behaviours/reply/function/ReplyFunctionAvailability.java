package behaviours.reply.function;

import behaviours.gather.GatherAvailableReply;
import behaviours.gather.GatherReplaceReply;
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
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

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
            String requireType = availableMessage.getRequiredType();
            int urgencyLevel = availableMessage.getUrgencyLevel();
            int period = availableMessage.getPeriod();
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
                if (requiredNum > serviceNum.get()) {
                    //这里添加替换模块
                    Tuple<Boolean, HashMap<String, Set<String>>> tuple = checkPossible2Replace();
                    if (tuple.a == true && urgencyLevel >= 3) {
                        int sendNum = 0;
                        try {
                            sendNum = sendCheckMsg2Rep(tuple.b);
                        } catch (JsonProcessingException e) {
                            throw new RuntimeException(e);
                        }
                        myAgent.addBehaviour(new GatherReplaceReply(sendNum, tuple.b, askAvailableMsg,
                                                                    new Map[]{highQualityRes, lowCostRes}, selectedAgg,
                                                                    availableNei, serviceNum));
                    } else {
                        replyContent.setType("fail");
                        System.out.println(myAgentName + "容量不足，无法提供服务");
                        try {
                            reply.setContent(mapper.writeValueAsString(replyContent));
                        } catch (JsonProcessingException e) {
                            throw new RuntimeException(e);
                        }
                        reply.addReceiver(askAvailableMsg.getSender());
                        myAgent.send(reply);
                    }

                } else {
//                    requireSuccess = true;
                    System.out.println("[请求]" + JadeUtil.getDateTime() + ":" + myAgentName + "容量足够，正在询问邻居容量");
                    try {
                        int MsgNum = sendAvailableMsg2Nei(availableMessage,
                                                          askAvailableMsg.getSender().getLocalName());
                        myAgent.addBehaviour(
                                new GatherAvailableReply(MsgNum, requiredNum, askAvailableMsg));
                    } catch (JsonProcessingException e) {
                        throw new RuntimeException(e);
                    }
                }
            }
            //如果是功能，且被访问过一次
//            if (!isResource && availableFlag.get() == true) {
////                System.out.println(myAgent);
////                System.out.println(JadeUtil.getAgentName(askAvailableMsg.getSender())+"重复请求");
//                ACLMessage reply = new ACLMessage(ACLMessage.INFORM);
//                AvailableMessage message = new AvailableMessage();
//                reply.setConversationId("answer-capacity-available");
//                message.setType("beAsked");
//                try {
//                    reply.setContent(mapper.writeValueAsString(message));
//                } catch (JsonProcessingException e) {
//                    throw new RuntimeException(e);
//                }
//                reply.addReceiver(askAvailableMsg.getSender());
//                myAgent.send(reply);
//
//            } else {
//                AvailableMessage availableMessage;
//                try {
//                    availableMessage = mapper.readValue(askAvailableMsg.getContent(),
//                                                        AvailableMessage.class);
//                } catch (IOException e) {
//                    throw new RuntimeException(e);
//                }
//                int requiredNum = availableMessage.getRequiredNum();
//                String requireType = availableMessage.getRequiredType();
//                //如果是资源
////                if (isResource) {
////                    neededNum.set(neededNum.get() + requiredNum);
////                } else {
////                    neededNum.set(requiredNum);
////                    availableFlag.set(true);
////                }
////            System.out.println(myAgentName+"需要提供："+neededNum);
//                if (requiredNum > serviceNum.get()) {
//                    ACLMessage answerAvailableMsg = new ACLMessage(ACLMessage.INFORM);
//                    AvailableMessage message = new AvailableMessage();
//                    answerAvailableMsg.setConversationId("answer-capacity-available");
//                    answerAvailableMsg.addReceiver(askAvailableMsg.getSender());
//                    System.out.println(myAgentName + "容量不足，无法提供服务");
//                    if (repFunction != null && repFunction.size() != 0) {
//                        Map.Entry<StringBuilder, Integer> lowCostRepEntry = lowCostRep.entrySet().iterator().next();
//                        Map.Entry<StringBuilder, Integer> highQualityRepEntry = highQualityRep.entrySet().iterator().next();
//                        StringBuilder lowCostRepName = lowCostRepEntry.getKey();
//                        int lowCostRepNum = lowCostRepEntry.getValue();
//                        StringBuilder highQualityName = highQualityRepEntry.getKey();
//                        int highQualityNum = highQualityRepEntry.getValue();
//                        System.out.println(myAgentName + "尝试替换功能");
//                        if (requireType.equals("lowCost")) {
//                            if (lowCostRepNum > requiredNum) {
//                                message.setType("replace");
//                                message.setReplaceAgent(String.valueOf(lowCostRepName));
//                                message.setRequiredNum(requiredNum);
//                                message.setRequiredType(requireType);
//                            } else {
//                                System.out.println(lowCostRepName + ":容量不足,替换失败");
//                                message.setType("fail");
//                            }
//                        } else {
//                            if (highQualityNum > requiredNum) {
//                                message.setType("replace");
//                                message.setReplaceAgent(String.valueOf(highQualityName));
//                                message.setRequiredNum(requiredNum);
//                                message.setRequiredType(requireType);
//                            } else {
//                                System.out.println(highQualityName + ":容量不足,替换失败");
//                                message.setType("fail");
//                            }
//                        }
//                    } else {
//                        System.out.println(myAgentName + "没有可替换的服务，请求失败");
//                        message.setType("fail");
//                    }
//                    try {
//                        answerAvailableMsg.setContent(mapper.writeValueAsString(message));
//                    } catch (JsonProcessingException e) {
//                        throw new RuntimeException(e);
//                    }
//                    myAgent.send(answerAvailableMsg);
//                } else {
//                    if (isResource) {
//                        //如果是资源，且能满足需求容量
//                        System.out.println(myAgentName + "容量足够，返回容量:" + serviceNum);
//                        ACLMessage answerAvailableMsg = new ACLMessage(ACLMessage.INFORM);
//                        AvailableMessage message = new AvailableMessage();
//                        answerAvailableMsg.setConversationId("answer-capacity-available");
//                        //设定报文内容
//                        message.setType("success");
//                        Map<String, Integer> mp = new HashMap<>();
//                        mp.put(myAgent.getName(), requiredNum);
//                        message.setRequiredAgent(mp);
//                        try {
//                            answerAvailableMsg.setContent(mapper.writeValueAsString(message));
//                        } catch (JsonProcessingException e) {
//                            throw new RuntimeException(e);
//                        }
//                        answerAvailableMsg.addReceiver(askAvailableMsg.getSender());
//                        myAgent.send(answerAvailableMsg);
//
//                    } else {
//                        System.out.println(myAgentName + "容量足够，正在询问邻居容量");
//                        AvailableMessage availableMessage1 = null;
//                        try {
//                            availableMessage1 = mapper.readValue(askAvailableMsg.getContent(),
//                                                                 AvailableMessage.class);
//                        } catch (IOException e) {
//                            throw new RuntimeException(e);
//                        }
//                        int MsgNum = 0;
//                        try {
//                            MsgNum = sendAvailableMsg2Nei(availableMessage1);
//                        } catch (JsonProcessingException e) {
//                            throw new RuntimeException(e);
//                        }
////                System.out.println(myAgentName+"发送"+sendNum+"个请求");
//                        //添加收集器
//                        myAgent.addBehaviour(
//                                new GatherAvailableReply(MsgNum, requiredNum, askAvailableMsg, offerDeque));
//                    }
//                }
//            }
        } else {
            block();
        }


    }

    private int sendAvailableMsg2Nei(AvailableMessage requestMessage, String asker) throws JsonProcessingException {
        int sendNum = 0;
        ACLMessage askAvailableMsg = new ACLMessage(ACLMessage.REQUEST);
        sendNum += addNei2Receivers(combFunction, asker, askAvailableMsg);
        sendNum += addNei2Receivers(depFunction, asker, askAvailableMsg);
//        sendNum += addNei2Receivers(resources, asker, askAvailableMsg);

        if (selectedAgg != null && selectedAgg.size() != 0) {

            Map.Entry<String, Integer> selectedAggAgent = selectedAgg.entrySet().iterator().next();
            String selectedAggName = selectedAggAgent.getKey();
            AID selectedAggAID = new AID(selectedAggName, AID.ISLOCALNAME);
//            selectedAggAID.setName(selectedAggName);
            askAvailableMsg.addReceiver(selectedAggAID);
            sendNum++;
        }
        String requireType = requestMessage.getRequiredType();
        String mAgentName = myAgent.getLocalName();
        if (resources != null && resources.size() != 0) {
            if (resources.size() == 1) {
                AID selectedResAID = new AID(resources.get(0).getLocalName(), AID.ISLOCALNAME);
//                System.out.println(myAgent.getLocalName() + "唯一的资源为：" + resources.get(0).getLocalName());
                System.out.println(
                        "[请求]" + JadeUtil.getDateTime() + ":" + mAgentName + "正在请求唯一资源：" + resources.get(
                                0).getLocalName());
                askAvailableMsg.addReceiver(selectedResAID);
                sendNum++;
            } else {
                Map.Entry<String, Integer> lowCostResAgent;
                String lowCostResName = null;
                Map.Entry<String, Integer> highQualityResAgent;
                String highQualityResName = null;
                if (lowCostRes != null && lowCostRes.size() != 0) {
                    lowCostResAgent = lowCostRes.entrySet().iterator().next();
                    lowCostResName = lowCostResAgent.getKey();
                }
                if (highQualityRes != null && highQualityRes.size() != 0) {
                    highQualityResAgent = highQualityRes.entrySet().iterator().next();
                    highQualityResName = highQualityResAgent.getKey();
                }
                if (requireType.equals("high-quality")) {
                    AID selectedResAID = new AID();
                    if (highQualityRes == null || highQualityRes.size() == 0) {
                        System.out.println(mAgentName + "只有低消耗资源：" + lowCostResName + "-正在请求");
                        selectedResAID.setLocalName(lowCostResName);
                    } else {
                        System.out.println(mAgentName + "正在请求高质量资源:" + highQualityResName);
                        selectedResAID.setLocalName(highQualityResName);
                    }
                    askAvailableMsg.addReceiver(selectedResAID);

                } else if (requireType.equals("low-cost")) {
                    AID selectedResAID = new AID();
                    if (lowCostRes == null || lowCostRes.size() == 0) {
                        System.out.println(mAgentName + "只有高质量资源" + highQualityResName + "-正在请求");
                        selectedResAID.setLocalName(highQualityResName);
                    } else {
                        System.out.println(mAgentName + "正在请求低消耗资源:" + lowCostResName);
                        selectedResAID.setLocalName(lowCostResName);
                    }
                    askAvailableMsg.addReceiver(selectedResAID);
                }
                sendNum++;
            }
        }

        askAvailableMsg.setConversationId("ask-capacity-available");
        askAvailableMsg.setContent(mapper.writeValueAsString(requestMessage));
//        askAvailableMsg.setContent(String.valueOf(requiredNum * serviceFactor) + "," + requiredType);
        myAgent.send(askAvailableMsg);
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
