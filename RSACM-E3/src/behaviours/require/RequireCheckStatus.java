package behaviours.require;

import behaviours.message.CheckMessage;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import jade.core.AID;
import jade.core.behaviours.Behaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import util.JadeUtil;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.atomic.AtomicInteger;

import static behaviours.gather.GatherCheckReply.append2file;

public class RequireCheckStatus extends Behaviour {
    static SimpleDateFormat dateFormat = new SimpleDateFormat("HH:mm:ss");
    public AID rootFunction;
    public AtomicInteger stepChain;
    int step = 1;
    int period;
    public static Map<String, Integer> updatedFunctions;
    ObjectMapper mapper = new ObjectMapper();
    int updated_num = 0;
    Set<String> updatedAgents ;
    int noiseRate;
    boolean init = false;
    public RequireCheckStatus(AtomicInteger stepChain, AID rootFunction,
            int period, Map<String, Integer> updatedFunctions,int noiseRate) {
        this.rootFunction = rootFunction;
        this.stepChain = stepChain;
        this.period = period;
        this.updatedFunctions = updatedFunctions;
        this.noiseRate=noiseRate;
    }
    public RequireCheckStatus(AtomicInteger stepChain, AID rootFunction,
            int period, Map<String, Integer> updatedFunctions,int noiseRate,boolean init) {
        this.rootFunction = rootFunction;
        this.stepChain = stepChain;
        this.period = period;
        this.updatedFunctions = updatedFunctions;
        this.noiseRate=noiseRate;
        this.init=init;
    }

    @Override
    public void action() {
        MessageTemplate template = MessageTemplate.and(MessageTemplate.MatchPerformative(ACLMessage.INFORM),
                                                       MessageTemplate.MatchConversationId("wake-up-to-check"));
        ACLMessage msg = myAgent.receive(template);
        if (msg != null || stepChain.get() == 0) {
            switch (step) {
                case 1:
                    System.out.println("\n-------------第" + period + "周期自检阶段开始-------------");
                    System.out.println(dateFormat.format(new Date()) + ":正在通知" + JadeUtil.getAgentName(
                            rootFunction) + "更新容量");
                    ACLMessage askCapacity = new ACLMessage(ACLMessage.REQUEST);
                    askCapacity.setConversationId("check-capacity");
                    CheckMessage checkMessage = new CheckMessage();
                    checkMessage.setRelationType("None");
                    checkMessage.setCheckMode("global");
                    checkMessage.setPeriod(period);
                    checkMessage.setRequirementID(0);
                    checkMessage.setProcessID(0);
//                    System.out.println("init="+init);
                    checkMessage.setInitFlag(init);
                    checkMessage.setNoiseRate(noiseRate);

                    try {
                        askCapacity.setContent(mapper.writeValueAsString(checkMessage));
                    } catch (JsonProcessingException e) {
                        throw new RuntimeException(e);
                    }
                    askCapacity.addReceiver(rootFunction);
//            askCapacity.setReplyWith("REQUEST" + System.currentTimeMillis());

                    myAgent.send(askCapacity);
                    step = 2;
                    break;
                case 2:
                    MessageTemplate checkCapacityMT = MessageTemplate.and(
                            MessageTemplate.MatchPerformative(ACLMessage.INFORM),
                            MessageTemplate.MatchConversationId("answer-capacity"));
                    ACLMessage check_reply = myAgent.receive(checkCapacityMT);
                    if (check_reply != null) {
                        step = 3;
                        try {
                            CheckMessage checkMessage1 = mapper.readValue(check_reply.getContent(),CheckMessage.class);
                            updated_num=checkMessage1.getUpdatedNum();
                            updatedAgents = checkMessage1.getUpdatedAgent();
                        } catch (IOException e) {
                            throw new RuntimeException(e);
                        }
                        System.out.println("-------------第" + period + "周期自检阶段结束-------------\n");
                        break;
                    } else {
                        block();
                    }
                    break;
                case 3:
                    break;
            }
        } else {
            block();
        }

    }

    @Override
    public boolean done() {
        if (step == 3) {
            if(init==false){
                String dir = JadeUtil.outputPath;
                String fileName1 = "状态更新次数-周期性-" + noiseRate + ".txt";
                append2file(dir + fileName1,
                            period + ":" + updatedAgents.size() + "\n");
                if(updatedAgents.size()!=updated_num){
                    System.out.println("[error]更新次数出错");
                }
                updatedFunctions.clear();
                myAgent.doWait(50);
                stepChain.getAndIncrement();
                ACLMessage aclMessage = new ACLMessage(ACLMessage.INFORM);
                aclMessage.setConversationId("wake-up-to-require-1-1");
                aclMessage.addReceiver(myAgent.getAID());
                myAgent.send(aclMessage);
            }else {

            }
//            System.out.println(stepChain);
            return true;
        } else {
            return false;
        }
    }
}
