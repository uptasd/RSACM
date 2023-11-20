package behaviours.reply;

import functionAgents.AgentAttributes;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import util.JadeUtil;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;

public class ReceiveIncreaseRequest extends GeneralCyclicService {
    private int releaseNum;
    private String agentName;

    public ReceiveIncreaseRequest(AgentAttributes agentAttributes) {
        super(agentAttributes);
    }


    @Override
    public void action() {
        MessageTemplate mt = MessageTemplate.and(MessageTemplate.MatchPerformative(ACLMessage.INFORM),
                                                 MessageTemplate.MatchConversationId("increase-capacity"));
        ACLMessage msg = myAgent.receive(mt);
        if (msg != null) {
            updateFlag.setLength(0);
            updateFlag.append("not-updated");
            agentName = JadeUtil.getAgentName(myAgent.getAID());
//            System.out.println(JadeUtil.getDateTime() + ":" + agentName + "收到释放通知！");
            releaseNum = Integer.parseInt(msg.getContent());
            Integer oldNum = serviceNum.get();
            serviceNum.set(oldNum + releaseNum);
            System.out.println(
                    "[释放]" + JadeUtil.getDateTime() + ":" + agentName + "容量增加" + releaseNum + ":" + oldNum + "->" + serviceNum.get());
//            sendUpdateMsg2Nei("增加", releaseNum);
            int newNum = serviceNum.get();
            if (newNum > 0) {

                String myName = getAgent().getLocalName();
                if(replacementMap.containsKey(myName)){
                    ArrayList<String> reps = replacementMap.get(myName);
                    synchronized (replaceView){
                        for (String rep : reps) {
                            Set<String> s = replaceView.get(rep);
                            if (s == null) {
                                s = new HashSet<>();
                                s.add(myName);
                                System.out.println("[替换视图]" + rep + "正在添加替换:" + myName);
                            } else if (!s.contains(myName)) {
                                s.add(myName);
                                System.out.println("[替换视图]" + rep + "正在添加替换:" + myName);
                            }
                            replaceView.put(rep, s);
                        }
                    }
                }
            }
        } else {
            block();
        }
    }

}
