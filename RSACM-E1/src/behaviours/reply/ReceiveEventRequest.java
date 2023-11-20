package behaviours.reply;

import behaviours.message.EventMessage;
import com.fasterxml.jackson.databind.ObjectMapper;
import functionAgents.AgentAttributes;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import util.JadeUtil;

import java.io.IOException;
import java.util.Random;

public class ReceiveEventRequest extends GeneralCyclicService {
    public ReceiveEventRequest(AgentAttributes agentAttributes) {
        super(agentAttributes);
    }

    @Override
    public void action() {
        MessageTemplate mt = MessageTemplate.and(MessageTemplate.MatchPerformative(ACLMessage.CFP),
                                                 MessageTemplate.MatchConversationId("generate-event"));
        ACLMessage msg = myAgent.receive(mt);
        if (msg != null) {
            updateFlag.setLength(0);
            updateFlag.append("not-updated");
            ObjectMapper mapper = new ObjectMapper();
            try {
                EventMessage eventMessage = mapper.readValue(msg.getContent(), EventMessage.class);
                int noiseRate = eventMessage.getNoiseRate();
                int period = eventMessage.getPeriod();
                int hour = period % 24;
                boolean workingFlag = false;
                String[] working_period = working_time.split(",");
                for (int i = 0; i < working_period.length; i++) {
                    int start = Integer.parseInt(working_period[i].split("-")[0]);
                    int end = Integer.parseInt(working_period[i].split("-")[1]);
                    if (hour <= end && hour >= start) {
                        workingFlag = true;
                    }
                }
                int ranNum1 = new Random().nextInt(100) + 1;
                int ranNum2 = new Random().nextInt(100) + 1;
//                System.out.println(ranNum1 + "," + ranNum2);
                EventMessage replyContent = new EventMessage();
                if (ranNum1 <= (100-noiseRate) && unavailableNum.get() > 0 && workingFlag) {
                    //按照噪声恢复容量
                    int oldServiceNum = serviceNum.get();
                    int unavailableCapacity = unavailableNum.get();
                    serviceNum.set(oldServiceNum + unavailableCapacity);
                    unavailableNum.set(0);
                    if (myAgent.getLocalName().equals("易慧敏-医生") || myAgent.getLocalName().equals("彭朝权-医生")) {
                        System.out.println(JadeUtil.getDateTime() + "[事件]" +
                                                   JadeUtil.getAgentName(myAgent) +
                                                   ":受到事件影响容量恢复：" +
                                                   oldServiceNum + "->" + serviceNum.get());

                    }
                } else if (ranNum2 <= noiseRate && serviceNum.get() > 0 && workingFlag) {
                    //根据噪声减少容量
                    int capacity = serviceNum.get();
                    int rs = capacity * noiseRate / 100;
                    if (rs <= 0) rs = 1;
                    unavailableNum.set(unavailableNum.get() + rs);
                    serviceNum.set(capacity - rs);
                    if (myAgent.getLocalName().equals("易慧敏-医生") || myAgent.getLocalName().equals("彭朝权-医生")) {
                        System.out.println(JadeUtil.getDateTime() + "[事件]" +
                                                   JadeUtil.getAgentName(myAgent) +
                                                   ":受到事件影响容量减少：" +
                                                   capacity + "->" + serviceNum.get());

                    }
                    replyContent.setAffectedFlag(true);
                    replyContent.setAffectedNum(rs);
                } else {
                    replyContent.setAffectedFlag(false);
                }
//                System.out.println("wtf");
                ACLMessage replyMSG = new ACLMessage(ACLMessage.INFORM);
                replyMSG.setConversationId("answer-event");
                replyMSG.setContent(mapper.writeValueAsString(replyContent));
                replyMSG.addReceiver(msg.getSender());
//                System.out.println(myAgent.getLocalName()+"回信");
                myAgent.send(replyMSG);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        } else {
            block();
        }
    }
}
