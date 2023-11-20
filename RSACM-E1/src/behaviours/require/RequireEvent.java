package behaviours.require;

import behaviours.message.EventMessage;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import jade.core.behaviours.Behaviour;
import jade.domain.DFService;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.domain.FIPAException;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;

import java.util.concurrent.atomic.AtomicInteger;

public class RequireEvent extends Behaviour {

    public AtomicInteger stepChain;
    public int noiseRate;
    private ObjectMapper mapper = new ObjectMapper();
    int step = 1;
    int resourceNum = 0;
    int replyCnt = 0;
    int period;

    public RequireEvent(AtomicInteger stepChain, int noiseRate, int period) {
        this.stepChain = stepChain;
        this.noiseRate = noiseRate;
        this.period = period;
    }

    @Override
    public void action() {
        switch (step) {
            case 1:
                System.out.println("-------------开始随机生成事件-------------");
                ACLMessage generateEvent = new ACLMessage(ACLMessage.CFP);
                generateEvent.setConversationId("generate-event");
                EventMessage message = new EventMessage();
                message.setNoiseRate(noiseRate);
                message.setPeriod(period);
                try {
                    generateEvent.setContent(mapper.writeValueAsString(message));
                } catch (JsonProcessingException e) {
                    throw new RuntimeException(e);
                }
                DFAgentDescription template = new DFAgentDescription();
                ServiceDescription resourceAgent = new ServiceDescription();
                resourceAgent.setType("resource");
                template.addServices(resourceAgent);
                try {
//                    SearchConstraints getAll = new SearchConstraints();
//                    getAll.setMaxResults(new Long(-1));
                    DFAgentDescription[] result1 = DFService.search(myAgent, template);
                    resourceNum = result1.length;
                    for (DFAgentDescription Agent : result1) {
                        generateEvent.addReceiver(Agent.getName());
//                        System.out.println("resource:" + Agent.getName().getLocalName());
                    }
                    myAgent.send(generateEvent);
                    step = 2;
                } catch (FIPAException e) {
                    throw new RuntimeException(e);
                }
//                break;
            case 2:
                MessageTemplate messageTemplate = MessageTemplate.and(
                        MessageTemplate.MatchPerformative(ACLMessage.INFORM),
                        MessageTemplate.MatchConversationId("answer-event"));
                ACLMessage eventReply = myAgent.receive(messageTemplate);
                if (eventReply != null) {
                    replyCnt++;
                    if (replyCnt >= resourceNum) {
                        step = 3;
                        break;
                    }
                }
                break;
            case 3:
                break;


        }
    }

    @Override
    public boolean done() {
        if (step == 3) {
            myAgent.doWait(50);
            stepChain.incrementAndGet();
            System.out.println("-------------随机事件结束-------------");
            ACLMessage aclMessage = new ACLMessage(ACLMessage.INFORM);
            aclMessage.setConversationId("wake-up-to-check");
            aclMessage.addReceiver(myAgent.getAID());
            myAgent.send(aclMessage);
            return true;
        } else {
            return false;
        }
    }
}
