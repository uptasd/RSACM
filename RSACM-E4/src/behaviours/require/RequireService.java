package behaviours.require;

import behaviours.message.AvailableMessage;
import behaviours.message.CheckMessage;
import behaviours.message.DecreaseMessage;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import jade.core.AID;
import jade.core.Agent;
import jade.core.behaviours.Behaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import util.RequirementInfo;
import util.JadeUtil;

import java.io.IOException;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;

import static behaviours.gather.GatherCheckReply.append2file;


public class RequireService extends Behaviour {
    //    static SimpleDateFormat dateFormat = new SimpleDateFormat("HH:mm:ss");
    private AID requiredFunction;
    //    private int repliesCnt = 0;
//    private MessageTemplate requireMT;
//    private MessageTemplate releaseMT;
//    private MessageTemplate responseIsAvailable;
//    private MessageTemplate checkCapacityMT;
    private int step = -1;
    private int requireNum = 1;
    private long requireTime;
    private int period;
    String requiredQos;
    Integer urgencyLevel;
    public AtomicInteger stepChain;
    private int processID;
    private int requirementID;
    private ObjectMapper mapper = new ObjectMapper();
    AtomicInteger succeedNum;
    AtomicInteger succeedPart;
    private Map<String, Integer> decreasedFunctions;
    private int sendDecreaseMsgNum;
    private int sendDecreaseMsgCnt = 0;
    public static Map<String, Integer> updatedFunctions;
    private boolean successFlag = true;
    long offset = 500;
    int endId;
    String nextRequirement;
    Set<String> waitSet = new HashSet<>() {{
        add("科室问诊_线上");
        add("科室问诊_线下");
        add("医疗诊断_线上");
        add("医疗诊断_线下");
        add("医疗检测_线下");
        add("医疗服务");
    }};
    int processCnt;
    int processNum;
    static Map<String, Integer> affectedAgent;
    static Map<String, Long> retrieveTime;
    static Map<String, Long> propagationTime;
    static Map<String, String> hitRate;
    long startTime;
    long endTime;
    //    long startTime2;
    long endTime2;
    int noiseRate;
    String hitRt = "";

    //endId是某一个请求的最后ID,processNum是整个周期的总请求数
    //processID是某个请求的id，processCnt是从第一个请求的第一个流程开始计数的
    public RequireService(int requirementID, AtomicInteger stepChain, int processID, int processCnt, int period, RequirementInfo requirementInfo, String nextRequirement,
            AtomicInteger succeedPart, AtomicInteger succeedNum, int endId, int processNum, Map<String, Integer> updatedFunctions,
            Map<String, Integer> affectedAgent, Map<String, Long> retrieveTime, Map<String, Long> propagationTime, Map<String, String> hitRate,
            int noiseRate) {
        this.requirementID = requirementID;
        this.stepChain = stepChain;
        this.processID = processID;
        this.period = period;
        this.requiredFunction = requirementInfo.getRequiredFunction();
//        this.requireNum = requireNum;
//        this.requireTime = requirementBean.getRequiredTime();
        if (requireTime >= 1) {
            this.requireTime = (long) (JadeUtil.getTimePeriod() * requirementInfo.getRequiredTime() - offset);
        } else {
            this.requireTime = (long) (JadeUtil.getTimePeriod() * requirementInfo.getRequiredTime());
        }
        this.requiredQos = requirementInfo.getRequireQos();
        this.urgencyLevel = requirementInfo.getUrgencyLevel();
        this.succeedNum = succeedNum;
        this.endId = endId;
        this.succeedPart = succeedPart;
        this.nextRequirement = nextRequirement;
        this.processCnt = processCnt;
        this.processNum = processNum;
        this.updatedFunctions = updatedFunctions;
        this.affectedAgent = affectedAgent;
        this.retrieveTime = retrieveTime;
        this.propagationTime = propagationTime;
        this.hitRate = hitRate;
        this.noiseRate = noiseRate;
    }

    @Override
    public void action() {
        MessageTemplate template = MessageTemplate.and(MessageTemplate.MatchPerformative(ACLMessage.INFORM),
                                                       MessageTemplate.MatchConversationId(
                                                               "wake-up-to-require" + "-" + period + "-" + processCnt));
        ACLMessage msg = myAgent.receive(template);
        if (stepChain.get() == processCnt || msg != null) {
            String rqID = period + "-" + requirementID;

            switch (step) {
                case -1:

                    System.out.println(JadeUtil.getDateTime() + ":" +
                                               ">>>>>>>第" + period + "个周期第" +
                                               requirementID + "个请求的第" +
                                               processID + "流程:" +
                                               requiredFunction.getLocalName() + "开始自检<<<<<<<");
                    if (!affectedAgent.containsKey(rqID)) {
                        affectedAgent.put(rqID, 0);
                    }
                    if (!retrieveTime.containsKey(rqID)) {
                        retrieveTime.put(rqID, 0L);
                    }
                    if (!propagationTime.containsKey(rqID)) {
                        propagationTime.put(rqID, 0L);
                    }
                    if (!hitRate.containsKey(rqID)) {
                        hitRate.put(rqID, "0/0");
                    }
                    ACLMessage askCapacity = new ACLMessage(ACLMessage.REQUEST);
                    askCapacity.setConversationId("check-capacity");
                    CheckMessage checkMessage = new CheckMessage();
                    checkMessage.setRelationType("None");
                    checkMessage.setPeriod(period);
                    checkMessage.setRequirementID(requirementID);
                    checkMessage.setProcessID(processID);
                    checkMessage.setCheckMode("normal");
                    try {
                        askCapacity.setContent(mapper.writeValueAsString(checkMessage));
                    } catch (JsonProcessingException e) {
                        throw new RuntimeException(e);
                    }
                    askCapacity.addReceiver(requiredFunction);
                    myAgent.send(askCapacity);
                    step = 0;
                    break;
                case 0:
                    MessageTemplate checkCapacityMT = MessageTemplate.and(
                            MessageTemplate.MatchPerformative(ACLMessage.INFORM),
                            MessageTemplate.MatchConversationId("answer-capacity"));
                    ACLMessage check_reply = myAgent.receive(checkCapacityMT);
                    if (check_reply != null) {
                        try {
                            CheckMessage checkMsg = mapper.readValue(check_reply.getContent(), CheckMessage.class);
//                            int unHitResNum = checkMsg.getUnHitResNum();
                            int requiredResNum = checkMsg.getRequiredResNum();
                            System.out.println(
                                    "[总资源数]" + rqID + ":" + requiredFunction.getLocalName() + "-" + requiredResNum);
                            int ResNum = Integer.parseInt(hitRate.get(rqID).split("/")[1]);
                            ResNum += requiredResNum;
                            hitRt = "/" + ResNum;
                        } catch (IOException e) {
                            throw new RuntimeException(e);
                        }
                        System.out.println(">>>>>>>" +
                                                   JadeUtil.getDateTime() + ":" + JadeUtil.getAgentName(
                                requiredFunction) + "自检结束<<<<<<<\n");
                        updatedFunctions.clear();
                        step = 1;
                    } else {
//                        block();
                    }
                    break;
                case 1:
                    startTime = System.currentTimeMillis();
                    System.out.println(
                            "************" + "尝试请求:" + requireNum + "个" + JadeUtil.getAgentName(
                                    requiredFunction) + "************");
                    ACLMessage askAvailable = new ACLMessage(ACLMessage.REQUEST);
                    askAvailable.addReceiver(requiredFunction);
                    askAvailable.setConversationId("ask-capacity-available");
//                    String requireType = "low-cost";
                    AvailableMessage availableMessage = new AvailableMessage();
                    availableMessage.setRequiredNum(requireNum);
                    availableMessage.setRequiredType(requiredQos);
                    availableMessage.setUrgencyLevel(urgencyLevel);
                    availableMessage.setPeriod(period);
                    availableMessage.setRequirementID(rqID);
                    try {
                        askAvailable.setContent(mapper.writeValueAsString(availableMessage));
                    } catch (JsonProcessingException e) {
                        throw new RuntimeException(e);
                    }
                    myAgent.send(askAvailable);
//                    System.out.println("stepChain="+stepChain.get());
                    step = 2;
                    break;
                case 2:
                    MessageTemplate availableReply = MessageTemplate.and(
                            MessageTemplate.MatchPerformative(ACLMessage.INFORM),
                            MessageTemplate.MatchConversationId("answer-capacity-available"));
                    ACLMessage availableReplyMsg = myAgent.receive(availableReply);
                    if (availableReplyMsg != null) {
                        try {
                            AvailableMessage replyAvailabilityMessage = mapper.readValue(availableReplyMsg.getContent(),
                                                                                         AvailableMessage.class);
                            String requireResult = replyAvailabilityMessage.getType();
                            int hitResNum = replyAvailabilityMessage.getHitResNum();
                            int hitNum = Integer.parseInt(hitRate.get(rqID).split("/")[0]);
                            hitNum += hitResNum;
                            System.out.println("[累计命中数]" + hitNum);
                            hitRt = hitNum + hitRt;
                            hitRate.put(rqID, hitRt);
                            System.out.println("requirement:" + requireResult);
                            endTime = System.currentTimeMillis();

                            System.out.println(
                                    "[总命中数]" + rqID + ":" + requiredFunction.getLocalName() + "-" + hitResNum);

                            System.out.println("[总命中率]" + hitRt);
                            long tmpl = retrieveTime.get(rqID);
                            tmpl += endTime - startTime;
                            retrieveTime.put(rqID, tmpl);

                            if (requireResult.equals("fail")) {
                                propagationTime.put(rqID, tmpl);
                                step = 5;
                            } else if (requireResult.equals("success")) {
//                                System.out.println("[命中率]" + "命中数：" + hitNum);
                                System.out.println("---------------" + JadeUtil.getAgentName(
                                        requiredFunction) + "请求服务成功，开始更新状态---------------");
//                                startTime2 = System.currentTimeMillis();
                                decreasedFunctions = replyAvailabilityMessage.getRequiredAgent();
                                sendDecreaseMsgNum = decreasedFunctions.size();
                                for (Map.Entry<String, Integer> entry : decreasedFunctions.entrySet()) {
                                    String functionAgentName = entry.getKey();
                                    int requiredNum = entry.getValue();
                                    //发送减少容量请求
                                    ACLMessage decreaseMsg = new ACLMessage(ACLMessage.CFP);
                                    decreaseMsg.setConversationId("decrease-capacity");
                                    AID agentAID = new AID();
                                    agentAID.setName(functionAgentName);
                                    decreaseMsg.addReceiver(agentAID);
                                    decreaseMsg.setContent(String.valueOf(requiredNum));
                                    myAgent.send(decreaseMsg);
                                }
                                step = 3;
                            } else if (requireResult.equals("replace")) {
                                AID replaceFun = new AID();
                                replaceFun.setName(replyAvailabilityMessage.getReplaceAgent());
                                requiredFunction = replaceFun;
                                step = 1;
                            }
                        } catch (IOException e) {
                            throw new RuntimeException(e);
                        }

//                        System.out.println(availableReplyMsg.getContent());

                    } else {
//                        block();
                    }
                    break;
                case 3:
                    //收集请求减少报文的回信
                    MessageTemplate decreaseReplyMT = MessageTemplate.and(
                            MessageTemplate.MatchPerformative(ACLMessage.INFORM),
                            MessageTemplate.MatchConversationId("response-decrease"));
                    ACLMessage decreaseReplyMsg = myAgent.receive(decreaseReplyMT);
                    if (decreaseReplyMsg != null) {
                        try {
                            DecreaseMessage replyContent = mapper.readValue(decreaseReplyMsg.getContent(),
                                                                            DecreaseMessage.class);
//                            System.out.println(replyContent.getType());
                            sendDecreaseMsgCnt++;
                            int decreasedNum = replyContent.getDecreasedNum();
                            String agentName = decreaseReplyMsg.getSender().getName();
                            decreasedFunctions.put(agentName, decreasedNum);
                            if (replyContent.getType().equals("success")) {

                            } else if (replyContent.getType().equals("fail")) {
                                successFlag = false;
                            }
                            if (sendDecreaseMsgCnt >= sendDecreaseMsgNum) {
                                endTime2 = System.currentTimeMillis();
                                long tmpl2 = propagationTime.get(rqID);
                                tmpl2 += endTime2 - startTime;
                                propagationTime.put(rqID, tmpl2);

                                if (successFlag == true) {
                                    succeedPart.set(succeedPart.get() + 1);
                                    int tmp = affectedAgent.get(rqID);
                                    tmp += decreasedFunctions.size();
                                    affectedAgent.put(rqID, tmp);
                                    step = 4;
                                } else {
                                    step = 5;
                                }
                            }
                        } catch (IOException e) {
                            throw new RuntimeException(e);
                        }
                    } else {
//                        block();
                    }
                    break;
                case 4:
                    //成功时进入
                    Timer timer = new Timer();
                    Agent mAgent = myAgent;
                    String releasedFunctionName = JadeUtil.getAgentName(requiredFunction);
//                    int p = period;
//                    int id = requiredID;
                    Map<String, Integer> releasedAgents = decreasedFunctions;
                    timer.schedule(new TimerTask() {
                        @Override
                        public void run() {
                            System.out.println(
                                    JadeUtil.getDateTime() + ":" + ">>>>>>>>>>开始释放第" + period + "周期第" + requirementID + "个请求的第" + processID + "流程：" + releasedFunctionName + "<<<<<<<<<<<");
                            for (Map.Entry<String, Integer> entry : releasedAgents.entrySet()) {
                                String agentName = entry.getKey();
                                Integer releaseNum = entry.getValue();
                                ACLMessage increaseMsg = new ACLMessage(ACLMessage.INFORM);
                                increaseMsg.setConversationId("increase-capacity");
                                increaseMsg.setContent(String.valueOf(releaseNum));
                                AID agentAID = new AID();
                                agentAID.setName(agentName);
                                increaseMsg.addReceiver(agentAID);
                                mAgent.send(increaseMsg);
                            }
                        }
                    }, requireTime);
                    step = 6;
                    break;
                case 5:
                    //失败时进入
                    System.out.println(
                            "************" + JadeUtil.getAgentName(requiredFunction) + "请求服务失败************");
                    //计算命中率
                    step = 6;
                    break;
                case 6:
                    if (processID == endId) {

                        if (succeedPart.get() == endId) {
                            succeedNum.set(succeedNum.get() + 1);
                            System.out.println(period + "周期第" + requirementID + "请求成功");
                        } else {
                            System.out.println(period + "周期第" + requirementID + "请求失败");
                        }
                        String dir = JadeUtil.outputPath;
                        String fileName1 = "状态更新次数-需求-" + noiseRate + ".txt";
                        String fileName2 = "检索资源时间-" + noiseRate + ".txt";
                        String fileName3 = "状态传播时间-" + noiseRate + ".txt";
                        String fileName4 = "命中率-" + noiseRate + ".txt";
                        String rqKey = period + "-" + requirementID;
                        append2file(dir + fileName1,
                                    rqKey + ":" + affectedAgent.get(rqKey) + "\n");
                        append2file(dir + fileName2,
                                    rqKey + ":" + retrieveTime.get(rqKey) + "\n");
                        append2file(dir + fileName3,
                                    rqKey + ":" + propagationTime.get(rqKey) + "\n");
                        append2file(dir + fileName4,
                                    rqKey + ":" + hitRate.get(rqKey) + "\n");
                    }
                    String[] functionSplit = requiredFunction.getLocalName().split("-");
                    String functionType = functionSplit[functionSplit.length - 1];
                    String[] nextFunSplit = nextRequirement.split("-");
                    String nextType = nextFunSplit[nextFunSplit.length - 1];
                    Boolean flag1 = waitSet.contains(functionType) && !functionType.equals("医疗检测_线下");
                    Boolean flag2 = waitSet.contains(nextType);
                    if (flag1 && flag2) {
                        long waitOffset = 50;
                        System.out.println(
                                period + "周期第" + requirementID + "请求的第" + processID + "流程开始暂停:" + (requireTime + waitOffset) + "毫秒");
                        myAgent.doWait(requireTime + waitOffset);
                        System.out.println(period + "周期第" + requirementID + "请求的第" + processID + "流程暂停结束");
                    }

                    step = 7;
                    break;

            }
        } else {
            block();
        }
    }

    @Override
    public boolean done() {
        if (step == 7) {
            if (processCnt != processNum) {
//                myAgent.doWait(50);
                stepChain.getAndIncrement();
//            System.out.println("end-stepChain=" + stepChain.get());
                ACLMessage msg = new ACLMessage(ACLMessage.INFORM);
                msg.setConversationId("wake-up-to-require-" + period + "-" + stepChain.get());
                msg.addReceiver(myAgent.getAID());
                myAgent.send(msg);
            }

            System.out.println("----开始处理下一个请求");
            return true;
        } else {
            return false;
        }
    }


}
