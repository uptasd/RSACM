package behaviours.gather;

import behaviours.message.AvailableMessage;
import behaviours.message.CheckMessage;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import jade.core.AID;
import jade.core.behaviours.Behaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;

import java.io.IOException;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;

public class GatherReplaceReply extends Behaviour {
    int sendNum;
    HashMap<String, Set<String>> RepFunctions;
    int step = 0;
    int replyCnt = 0;
    HashMap<String, String> repOfFailedFun = new HashMap<>();
    //    int possibleNum = 0;
    ACLMessage askAvailableMsgFromUp;
    private Map<String, Integer> highQualityRes;
    private Map<String, Integer> lowCostRes;
    private Map<String, Integer> selectedAgg;
    public ArrayList<String> availableNei;
    public AtomicInteger serviceNum;
    //用来收集回复信息中的失效agent
    // 如果这个集合数量大于等于(其实只需要等于)，那代表所有的失效agent都有对应的容量大于0的替换agent

    public Set<String> succeedFailAgentSet = new HashSet<>();
    ObjectMapper mapper = new ObjectMapper();

    public GatherReplaceReply(int sendNum, HashMap<String, Set<String>> RepFunctions,
            ACLMessage askAvailableMsgFromUp, Map[] resources, Map<String, Integer> selectedAgg,
            ArrayList<String> availableNei, AtomicInteger serviceNum) {
        this.sendNum = sendNum;
        this.RepFunctions = RepFunctions;
        this.askAvailableMsgFromUp = askAvailableMsgFromUp; //来自父节点的ask请求
        this.highQualityRes = resources[0];
        this.lowCostRes = resources[1];
        this.selectedAgg = selectedAgg;
        this.availableNei = availableNei;
        this.serviceNum = serviceNum;
    }

    @Override
    public void action() {
        MessageTemplate AnswerMT = MessageTemplate.and(MessageTemplate.MatchPerformative(ACLMessage.INFORM),
                                                       MessageTemplate.MatchConversationId("answer-capacity2Rep"));
        switch (step) {
            case 0:
                ACLMessage answerCapacity = myAgent.receive(AnswerMT);
                if (answerCapacity != null) {
                    replyCnt++;
                    String replyAgentName = answerCapacity.getSender().getLocalName();
                    CheckMessage replyCheckMSg;
                    try {
                        replyCheckMSg = mapper.readValue(answerCapacity.getContent(), CheckMessage.class);
                    } catch (IOException e) {
                        throw new RuntimeException(e);
                    }
                    String replyContent = answerCapacity.getContent();
                    int replyServiceNum = replyCheckMSg.getServiceNum();
                    String failedAgentName = replyCheckMSg.getFailedAgentName();
                    System.out.println(
                            "[替换]" + myAgent.getLocalName() + "收到" + failedAgentName + "的替换：" + replyAgentName + "容量为:" + replyServiceNum);
                    if (replyServiceNum > 0) {
                        repOfFailedFun.put(failedAgentName, replyAgentName);
                        succeedFailAgentSet.add(failedAgentName);
//                        possibleNum++;
                    }
                    if (replyCnt >= sendNum) {
                        System.out.println("[替换]" + myAgent.getLocalName() + "的所有失效agent的替换功能已全部回信");
                        if (succeedFailAgentSet.size() >= RepFunctions.size()) {
                            System.out.println("[替换]" + myAgent.getLocalName() + "的所有失效agent都能找到可用的替换");
                            ACLMessage askAvailable = new ACLMessage(ACLMessage.REQUEST);
                            askAvailable.setConversationId("ask-capacity-available");
                            AvailableMessage availableMessage = new AvailableMessage();
                            availableMessage.setRequiredNum(1);
                            availableMessage.setRequiredType("low-cost");
                            availableMessage.setUrgencyLevel(0);
                            for (Map.Entry<String, String> entry : repOfFailedFun.entrySet()) {
                                String failedFun = entry.getKey();
                                String repFun = entry.getValue();
                                System.out.println(
                                        "[替换]" + myAgent.getLocalName() + "开始替换:" + failedFun + "->" + repFun);
                                askAvailable.addReceiver(new AID(repFun, AID.ISLOCALNAME));
                            }

                            if ((highQualityRes != null && !highQualityRes.isEmpty()) || (lowCostRes != null && !lowCostRes.isEmpty())) {
                                try {
                                    AvailableMessage askFromUp = mapper.readValue(askAvailableMsgFromUp.getContent(),
                                                                                  AvailableMessage.class);
                                    String requireType = askFromUp.getRequiredType();
                                    Map.Entry<String, Integer> lowCostResAgent;
                                    String lowCostResName = null;
                                    Map.Entry<String, Integer> highQualityResAgent;
                                    String highQualityResName = null;
                                    String mAgentName = myAgent.getLocalName();
                                    if (lowCostRes != null && lowCostRes.size() != 0) {
                                        lowCostResAgent = lowCostRes.entrySet().iterator().next();
                                        lowCostResName = lowCostResAgent.getKey();
                                    }
                                    if (highQualityRes != null && highQualityRes.size() != 0) {
                                        highQualityResAgent = highQualityRes.entrySet().iterator().next();
                                        highQualityResName = highQualityResAgent.getKey();
                                    }
                                    AID selectedResAID = new AID();
                                    if (requireType.equals("high-quality")) {
                                        if (highQualityRes == null || highQualityRes.size() == 0) {
                                            System.out.println(mAgentName + "只有低消耗资源：" + lowCostResName + "-正在请求");
                                            selectedResAID.setLocalName(lowCostResName);
                                        } else {
                                            System.out.println(mAgentName + "正在请求高质量资源:" + highQualityResName);
                                            selectedResAID.setLocalName(highQualityResName);
                                        }
//                                        askAvailable.addReceiver(selectedResAID);
                                    } else if (requireType.equals("low-cost")) {
//                                        AID selectedResAID = new AID();
                                        if (lowCostRes == null || lowCostRes.size() == 0) {
                                            System.out.println(mAgentName + "只有高质量资源" + highQualityResName + "-正在请求");
                                            selectedResAID.setLocalName(highQualityResName);
                                        } else {
                                            System.out.println(mAgentName + "正在请求低消耗资源:" + lowCostResName);
                                            selectedResAID.setLocalName(lowCostResName);
                                        }
//                                        askAvailable.addReceiver(selectedResAID);
                                    }
                                    askAvailable.addReceiver(selectedResAID);
                                } catch (IOException e) {
                                    throw new RuntimeException(e);
                                }
                            }
                            if (selectedAgg != null && !selectedAgg.isEmpty()) {
                                Map.Entry<String, Integer> selectedAggAgent = selectedAgg.entrySet().iterator().next();
                                String selectedAggName = selectedAggAgent.getKey();
                                AID selectedAggAID = new AID(selectedAggName, AID.ISLOCALNAME);
//            selectedAggAID.setName(selectedAggName);
                                askAvailable.addReceiver(selectedAggAID);
                            }
                            for (String agent : availableNei) {
                                System.out.println(myAgent.getLocalName() + "请求:" + agent);
                                AID aid = new AID(agent, AID.ISLOCALNAME);
                                askAvailable.addReceiver(aid);
                            }
                            try {
                                askAvailable.setContent(mapper.writeValueAsString(availableMessage));
                            } catch (JsonProcessingException e) {
                                throw new RuntimeException(e);
                            }
                            Iterator ite = askAvailable.getAllReceiver();
                            int sendNum = 0;
                            while (ite.hasNext()) {
                                ite.next();
                                sendNum++;
                            }
                            myAgent.send(askAvailable);
                            myAgent.addBehaviour(
                                    new GatherAvailableReply(sendNum, 1, askAvailableMsgFromUp));
                            serviceNum.set(1);
                            step = 1;
                        } else {
                            System.out.println(myAgent.getLocalName() + "替换失败");
                            ACLMessage reply = new ACLMessage(ACLMessage.INFORM);
                            reply.setConversationId("answer-capacity-available");
                            AvailableMessage replyContent2Up = new AvailableMessage();
                            replyContent2Up.setType("fail");
                            reply.addReceiver(askAvailableMsgFromUp.getSender());
                            try {
                                reply.setContent(mapper.writeValueAsString(replyContent2Up));
                            } catch (JsonProcessingException e) {
                                throw new RuntimeException(e);
                            }
                            myAgent.send(reply);
                        }
                    }
                }
        }

    }

    @Override
    public boolean done() {
        return false;
    }
}
