package behaviours.gather;

import behaviours.message.AvailableMessage;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import jade.core.behaviours.Behaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class GatherAvailableReply extends Behaviour {
    int step = 1;
    int sendNum;
    int receiveCnt = 0;
    int requiredNum = 0;
    boolean isAvailable = true;
    ACLMessage isAvailableMsg;
    //    public Deque<List<String>> offerDeque;
//    public ArrayList<AID> repFunction;
    public List<String> failedFunctions = new ArrayList<>();
    private HashMap<String, Integer> availableAgentMap = new HashMap<>();
    ObjectMapper mapper = new ObjectMapper();
    //    public static Map<String, ArrayList<String>> replacementMap;
//    public ArrayList<ReplaceBean> replaceBeans = new ArrayList<>();
//    public Map<String, Integer> replyCnt = new HashMap<>();
//    public Map<String, ReplyReplaceBean> ReplyReplaceMap = new HashMap<>();
//    int sendRepNum = 0;
//    int requireReplaceNum;
//    int requireReplaceCnt;
//    HashMap<String, Set<String>> neiSet;
    int totalHitNum = 0;

    public GatherAvailableReply(int sendNum, int requiredNum, ACLMessage isAvailableMsg) {
        //sendNum：the number of send msg to compare with the reply msg
        this.sendNum = sendNum;
        this.requiredNum = requiredNum;
        this.isAvailableMsg = isAvailableMsg;
//        this.repFunction = repFunction;
//        this.replacementMap = replacementMap;
    }


    @Override
    public void action() {
        MessageTemplate mt = MessageTemplate.and(MessageTemplate.MatchPerformative(ACLMessage.INFORM),
                                                 MessageTemplate.MatchConversationId("answer-capacity-available"));
        switch (step) {
            case 1:
                ACLMessage msg = myAgent.receive(mt);
                if (msg != null) {
//                    System.out.println(
//                            JadeUtil.getAgentName(myAgent) + "收到" + JadeUtil.getAgentName(msg.getSender()) + "的回信");
                    receiveCnt++;
                    AvailableMessage message;
                    try {
                        message = mapper.readValue(msg.getContent(), AvailableMessage.class);
                    } catch (IOException e) {
                        throw new RuntimeException(e);
                    }
                    String type = message.getType();
                    totalHitNum += message.getHitResNum();
                    if (type.equals("fail")) {
                        failedFunctions.add(msg.getSender().getLocalName());
                        isAvailable = false;
//                        step = 2;
                    } else if (type.equals("success")) {
//                        offerList.add(msg.getSender().getName());
                        Map<String, Integer> neiMap = message.getRequiredAgent();
                        for (Map.Entry<String, Integer> entry : neiMap.entrySet()) {
                            String agentName = entry.getKey();
                            Integer requiredFre = entry.getValue();
                            Integer tmp = 0;
                            if (availableAgentMap.containsKey(agentName)) {
                                tmp = availableAgentMap.get(agentName);
                            }
                            availableAgentMap.put(agentName, tmp + requiredFre);

                        }
                    } else if (type.equals("beAsked")) {
//                        System.out.println(msg.getSender().getName());
                    }

                    if (receiveCnt >= sendNum) {
                        step = 7;

                    }
                } else {
                    block();
                }
                break;
            case 7:
                ACLMessage reply = new ACLMessage(ACLMessage.INFORM);
                AvailableMessage replyMessage = new AvailableMessage();
                reply.setConversationId("answer-capacity-available");
                replyMessage.setHitResNum(totalHitNum);
                if (isAvailable) {
//                    System.out.println("将成功信息返回给上一级");
                    replyMessage.setType("success");
                    availableAgentMap.put(myAgent.getName(), requiredNum);
                    replyMessage.setRequiredAgent(availableAgentMap);

                } else {
                    replyMessage.setType("fail");
                }

                try {
                    reply.setContent(mapper.writeValueAsString(replyMessage));
                } catch (JsonProcessingException e) {
                    throw new RuntimeException(e);
                }
                //将结果发回给请求者
                reply.addReceiver(isAvailableMsg.getSender());
                myAgent.send(reply);
                step = 8;
        }

    }


    @Override
    public boolean done() {
        return (step == 8);
    }
}
