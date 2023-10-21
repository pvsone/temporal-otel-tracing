from datetime import timedelta

from temporalio import activity, workflow


@workflow.defn
class GreetingWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        return await workflow.execute_activity(
            compose_greeting,
            name,
            start_to_close_timeout=timedelta(seconds=10),
        )


@activity.defn
async def compose_greeting(name: str) -> str:
    return f"Hello, {name}!"
