package resourceAgents;

import behaviours.reply.ReceiveDecreaseRequest;
import behaviours.reply.ReceiveEventRequest;
import behaviours.reply.ReceiveIncreaseRequest;
import behaviours.reply.resource.ReplyResourceAvailability;
import behaviours.reply.resource.ReplyResourceStatus;
import functionAgents.AgentAttributes;
import jade.core.Agent;
import util.JadeUtil;
import util.ResourceBean;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;

public class ResourceAgent extends Agent {
    //    public Boolean isResource=true;
//    public AtomicInteger neededNum=new AtomicInteger(0);
//    public AtomicBoolean decreasedFlag = new AtomicBoolean(false);
//    public AtomicBoolean increaseFlag = new AtomicBoolean(false);
//    public AtomicBoolean availableFlag = new AtomicBoolean(false);
    public AtomicInteger unavailableNum = new AtomicInteger(0);
    public AtomicInteger recoveryNum = new AtomicInteger(0);
    public String resourceType = "low-cost";
    public StringBuilder updateFlag = new StringBuilder("not-updated");
    private AtomicInteger serviceNum = new AtomicInteger();
    private String working_time = "8-18";
    private Map<Integer, Integer> periodStatus = new HashMap<>();
    AtomicInteger last_serviceNum = new AtomicInteger();

    @Override
    protected void setup() {
        ResourceBean arguments = (ResourceBean) getArguments()[0];
        int serviceCapacity = arguments.getServiceNum();
        working_time = arguments.getWorking_time();
        resourceType = arguments.getResourceType();
        serviceNum.set(serviceCapacity);
        AgentAttributes agentAttributes = new AgentAttributes()
                .unavailableNum(unavailableNum)
                .recoveryNum(recoveryNum)
                .updateFlag(updateFlag)
                .resourceType(resourceType)
                .working_time(working_time)
                .periodStatus(periodStatus)
                .last_serviceNum(last_serviceNum)
                .serviceNum(serviceNum);

        addBehaviour(new ReplyResourceStatus(agentAttributes));
        addBehaviour(new ReplyResourceAvailability(agentAttributes));
        addBehaviour(new ReceiveDecreaseRequest(agentAttributes));
        addBehaviour(new ReceiveIncreaseRequest(agentAttributes));
        addBehaviour(new ReceiveEventRequest(agentAttributes));
//        doWait(10);
//        int hour = 1;
//        String[] working_period = working_time.split(",");
//        boolean workingFlag = false;
//        for (int i = 0; i < working_period.length; i++) {
//            int start = Integer.parseInt(working_period[i].split("-")[0]);
//            int end = Integer.parseInt(working_period[i].split("-")[1]);
//            if (hour <= end && hour >= start) {
//                workingFlag = true;
//            }
//        }
        JadeUtil.register_service(this, "resource", getLocalName());
//        System.out.println(getAID().getName() + "已加载，容量为:" + serviceCapacity);
    }
}
