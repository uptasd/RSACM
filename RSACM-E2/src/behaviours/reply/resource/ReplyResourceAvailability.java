package behaviours.reply.resource;

import behaviours.message.AvailableMessage;
import behaviours.reply.GeneralCyclicService;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import functionAgents.AgentAttributes;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class ReplyResourceAvailability extends GeneralCyclicService {
    public ReplyResourceAvailability(AgentAttributes agentAttributes) {
        super(agentAttributes);
    }

    ObjectMapper mapper = new ObjectMapper();

    @Override
    public void action() {
        MessageTemplate mt = MessageTemplate.and(MessageTemplate.MatchPerformative(ACLMessage.REQUEST),
                                                 MessageTemplate.MatchConversationId("ask-capacity-available"));
        ACLMessage askAvailableMsg = myAgent.receive(mt);
        if (askAvailableMsg != null) {
            AvailableMessage availableMessage;
            try {
                availableMessage = mapper.readValue(askAvailableMsg.getContent(), AvailableMessage.class);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            int requiredNum = availableMessage.getRequiredNum();
//            System.out.println(JadeUtil.getAgentName(myAgent) + "require:" + requiredNum);
            ACLMessage reply = new ACLMessage(ACLMessage.INFORM);
            reply.setConversationId("answer-capacity-available");
            AvailableMessage replyContent = new AvailableMessage();
            if (serviceNum.get() >= requiredNum) {
                Map<String, Integer> mp = new HashMap<>();
                mp.put(myAgent.getName(), requiredNum);
                replyContent.setType("success");
                replyContent.setRequiredAgent(mp);
                replyContent.setHitResNum(1);
                System.out.println("[请求]" + myAgent.getLocalName() + "收到请求" + requiredNum + "个请求：容量足够");
            } else {
                replyContent.setType("fail");
                replyContent.setHitResNum(0); //在有自检的情况下，这里应该不会被用到
                System.out.println(
                        "[请求]" + myAgent.getLocalName() + "响应请求" + requiredNum + "个失败，自身容量为：" + serviceNum.get());
            }
            try {
                reply.setContent(mapper.writeValueAsString(replyContent));
            } catch (JsonProcessingException e) {
                throw new RuntimeException(e);
            }
            reply.addReceiver(askAvailableMsg.getSender());
            myAgent.send(reply);
        }
    }
}
