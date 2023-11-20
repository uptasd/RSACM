package behaviours.reply;

import behaviours.message.DecreaseMessage;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import functionAgents.AgentAttributes;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import util.JadeUtil;

import java.util.ArrayList;
import java.util.Set;

public class ReceiveDecreaseRequest extends GeneralCyclicService {
    //该类对应于requireService中的case 0，用于接收需求agent的请求信息，减少资源容量后，通知相关的agent减少容量

    private int requiredNum;
    private String agentName;
    private ObjectMapper mapper = new ObjectMapper();

    //    public ReceiveDecreaseQuest(AID[] combFunction, AID[] aggFunction, AID[] depFunction, AID[] repFunction, AID[] resources,
//            Deque<String> aggQueue, StringBuilder selectedAgg, AtomicInteger serviceNum) {
//        super(combFunction, aggFunction, depFunction, repFunction, resources, aggQueue,selectedAgg, serviceNum);
//    }
    public ReceiveDecreaseRequest(AgentAttributes agentAttributes) {
        super(agentAttributes);
    }

    int step = 0;

    @Override
    public void action() {
        MessageTemplate mt = MessageTemplate.and(MessageTemplate.MatchPerformative(ACLMessage.CFP),
                                                 MessageTemplate.MatchConversationId("decrease-capacity"));
        ACLMessage msg = myAgent.receive(mt);
        if (msg != null) {
//            if (!isResource) {
//                decreasedFlag.set(true);
//            }
//            System.out.println("getContent::00-" + msg.getContent());
//            updateFlag.setLength(0);
//            updateFlag.append("not-updated");
            requiredNum = Integer.parseInt(msg.getContent());
            ACLMessage reply = new ACLMessage(ACLMessage.INFORM);
            DecreaseMessage replyContent = new DecreaseMessage();
            reply.setConversationId("response-decrease");
            if (requiredNum > serviceNum.get()) {
                System.out.println("[更新]" + JadeUtil.getAgentName(myAgent) + "容量不足，无法提供服务");
                //功能的容量没有意义，能触发减少容量的步骤说明，前面的可用性判断一定是通过了
                replyContent.setType("success");
                int oldNum = serviceNum.get();
                serviceNum.set(oldNum - 0);
                System.out.println("[更新]" + JadeUtil.getDateTime() + ":" +
                                           JadeUtil.getAgentName(myAgent) + "提供服务后，容量：" + oldNum + "->" + serviceNum.get());
                replyContent.setDecreasedNum(0);
            } else {
                replyContent.setType("success");
                agentName = JadeUtil.getAgentName(myAgent.getAID());
//                        System.out.println(
//                                JadeUtil.getDateTime() + ":" + agentName + "能提供" + serviceNum.get() + "个服务");
                //更新自身的服务容量
                int oldNum = serviceNum.get();
                serviceNum.set(oldNum - requiredNum);
                System.out.println("[更新]" + JadeUtil.getDateTime() + ":" +
                                           JadeUtil.getAgentName(myAgent) + "提供服务后，容量：" + oldNum + "->" + serviceNum.get());
//                sendUpdateMsg2Nei("减少", requiredNum);
                int newNum = serviceNum.get();
                String myName = getAgent().getLocalName();
                replyContent.setDecreasedNum(requiredNum);
                if (newNum == 0) {
                    if(replacementMap.containsKey(myName)){
                        ArrayList<String> reps = replacementMap.get(myName);
                        synchronized (replaceView){
                            for (String rep : reps) {
                                Set<String> s = replaceView.get(rep);
                                if(s!=null){
                                    if(s.contains(myName)){
                                        System.out.println("[替换]" + rep + "的替换去除：" + myName);
                                        s.remove(myName);
                                    }
                                    replaceView.put(rep,s);
                                }
                            }
                        }
                    }
                }
            }
            reply.addReceiver(msg.getSender());
            if (availableFlag != null) {
                availableFlag.set(false);
            }
            if (neededNum != null) {
                neededNum.set(0);
            }
            try {
                reply.setContent(mapper.writeValueAsString(replyContent));
            } catch (JsonProcessingException e) {
                throw new RuntimeException(e);
            }
            myAgent.send(reply);
//            System.out.println("bestAggAgent:"+JadeUtil.getAgentName(bestAggAgent));

        } else {
            block();
        }
    }

}
