package behaviours.reply.resource;

import behaviours.message.CheckMessage;
import behaviours.reply.GeneralCyclicService;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import functionAgents.AgentAttributes;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import util.JadeUtil;

import java.io.IOException;

import static behaviours.gather.GatherCheckReply.append2file;

public class ReplyResourceStatus extends GeneralCyclicService {
    public ReplyResourceStatus(AgentAttributes agentAttributes) {
        super(agentAttributes);
    }

    static ObjectMapper mapper = new ObjectMapper();

    @Override
    public void action() {
        MessageTemplate checkMT = MessageTemplate.and(MessageTemplate.MatchPerformative(ACLMessage.REQUEST),
                                                      MessageTemplate.MatchConversationId("check-capacity"));
        ACLMessage checkMsg = myAgent.receive(checkMT);
        if (checkMsg != null) {

            String myName = JadeUtil.getAgentName(myAgent.getAID());
//            if (mAgentName.equals("中山大学第三附属医院-服务大厅"))
//                System.out.println(mAgentName + "收到" + checkMsg.getSender().getLocalName() + "的请求");
            CheckMessage requireCheckMsg;
            try {
                requireCheckMsg = mapper.readValue(checkMsg.getContent(), CheckMessage.class);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            String checkMode = requireCheckMsg.getCheckMode();
            int period = requireCheckMsg.getPeriod();
            int hour = period % 24;
            int noiseRate = requireCheckMsg.getNoiseRate();
            String[] working_period = working_time.split(",");
//            if(myName.equals("杨晓燕-医生")){
//                System.out.println("here");
//            }
            boolean workingFlag = false;
            for (int i = 0; i < working_period.length; i++) {
                int start = Integer.parseInt(working_period[i].split("-")[0]);
                int end = Integer.parseInt(working_period[i].split("-")[1]);
                if (hour <= end && hour >= start) {
                    workingFlag = true;
                }
            }
            int sNum = serviceNum.get();
            int rNum = recoveryNum.get();
            if (workingFlag == false && sNum > 0) {
                recoveryNum.set(sNum + rNum);
                serviceNum.set(0);
            } else if (workingFlag == true && rNum > 0) {
                serviceNum.set(recoveryNum.get());
                recoveryNum.set(0);
            }
            ACLMessage reply = new ACLMessage(ACLMessage.INFORM);
            reply.setConversationId("answer-capacity");
            CheckMessage replyCheckMessage = new CheckMessage();
            replyCheckMessage.setRelationType("add");
            replyCheckMessage.setResourceType(resourceType);
            replyCheckMessage.setServiceNum(serviceNum.get());
//            if (workingFlag == false) {
//                replyCheckMessage.setServiceNum(0);
//            } else {
//                replyCheckMessage.setServiceNum(serviceNum.get());
//            }

            ObjectMapper mapper = new ObjectMapper();
            try {
                reply.setContent(mapper.writeValueAsString(replyCheckMessage));
            } catch (JsonProcessingException e) {
                throw new RuntimeException(e);
            }
            reply.addReceiver(checkMsg.getSender());
//                System.out.println("资源" + mAgentName + "将自身状态返回给" + askerName);
            if (updateFlag.toString().equals("not-updated")) {
                updateFlag.setLength(0);
                updateFlag.append("updated");
//                System.out.println("[自检]" + "资源" + mAgentName + "容量为" + serviceNum.get());
            }

            if (myName.equals("彭朝权-医生") && checkMode.equals("global")) {
                System.out.println("[]" + checkMsg.getSender().getLocalName() + "发送请求");
                String dir = JadeUtil.outputPath;
                String fileName = "彭朝权-医生-"+noiseRate+".txt";
                append2file(dir + fileName,
                            period + ":" + serviceNum.get() + "\n");
            }
            if (myName.equals("杨晓燕-医生") && checkMode.equals("global")) {
                System.out.println("[]" + checkMsg.getSender().getLocalName() + "发送请求");
                String dir = JadeUtil.outputPath;
                String fileName = "杨晓燕-医生-"+noiseRate+".txt";
                append2file(dir + fileName,
                            period + ":" + serviceNum.get() + "\n");
            }
            myAgent.send(reply);
        }
    }
}
