import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class tcolors:
    OKBLUE: str = "\033[94m"
    HEADER: str = "\033[95m"
    OKGREEN: str = "\033[92m"
    WARNING: str = "\033[93m"
    FAIL: str = "\033[91m"
    ENDC: str = "\033[0m"
    BOLD: str = "\033[1m"
    UNDERLINE: str = "\033[4m"


class ConsoleLogger:
    def __init__(self):
        # TODO: color code for value changes
        # use these to compare values between iterations
        self.old_train_loss_dict = None
        self.old_epoch_loss_dict = None
        self.old_eval_loss_dict = None

    # pylint: disable=no-self-use
    def get_time(self):
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def print_epoch_start(self, epoch, max_epoch, output_path=None):
        print(
            "\n{}{} > EPOCH: {}/{}{}".format(tcolors.UNDERLINE, tcolors.BOLD, epoch, max_epoch, tcolors.ENDC),
            flush=True,
        )
        if output_path is not None:
            print(f" --> {output_path}")

    def print_train_start(self):
        print(f"\n{tcolors.BOLD} > TRAINING ({self.get_time()}) {tcolors.ENDC}")

    def print_train_step(self, batch_steps, step, global_step, loss_dict, avg_loss_dict):
        indent = "     | > "
        print()
        log_text = "{}   --> STEP: {}/{} -- GLOBAL_STEP: {}{}\n".format(
            tcolors.BOLD, step, batch_steps, global_step, tcolors.ENDC
        )
        for key, value in loss_dict.items():
            # print the avg value if given
            if f"avg_{key}" in avg_loss_dict.keys():
                log_text += "{}{}: {:.5f}  ({:.5f})\n".format(indent, key, value, avg_loss_dict[f"avg_{key}"])
            else:
                log_text += "{}{}: {:.5f} \n".format(indent, key, value)
        print(log_text, flush=True)

    # pylint: disable=unused-argument
    def print_train_epoch_end(self, global_step, epoch, epoch_time, print_dict):
        indent = "     | > "
        log_text = f"\n{tcolors.BOLD}   --> TRAIN PERFORMACE -- EPOCH TIME: {epoch_time:.2f} sec -- GLOBAL_STEP: {global_step}{tcolors.ENDC}\n"
        for key, value in print_dict.items():
            log_text += "{}{}: {:.5f}\n".format(indent, key, value)
        print(log_text, flush=True)

    def print_eval_start(self):
        print(f"\n{tcolors.BOLD} > EVALUATION {tcolors.ENDC}\n")

    def print_eval_step(self, step, loss_dict, avg_loss_dict):
        indent = "     | > "
        log_text = f"{tcolors.BOLD}   --> STEP: {step}{tcolors.ENDC}\n"
        for key, value in loss_dict.items():
            # print the avg value if given
            if f"avg_{key}" in avg_loss_dict.keys():
                log_text += "{}{}: {:.5f}  ({:.5f})\n".format(indent, key, value, avg_loss_dict[f"avg_{key}"])
            else:
                log_text += "{}{}: {:.5f} \n".format(indent, key, value)
        print(log_text, flush=True)

    def print_epoch_end(self, epoch, avg_loss_dict):
        indent = "     | > "
        log_text = "\n  {}--> EVAL PERFORMANCE{}\n".format(tcolors.BOLD, tcolors.ENDC)
        for key, value in avg_loss_dict.items():
            # print the avg value if given
            color = ""
            sign = "+"
            diff = 0
            if self.old_eval_loss_dict is not None and key in self.old_eval_loss_dict:
                diff = value - self.old_eval_loss_dict[key]
                if diff < 0:
                    color = tcolors.OKGREEN
                    sign = ""
                elif diff > 0:
                    color = tcolors.FAIL
                    sign = "+"
            log_text += "{}{}:{} {:.5f} {}({}{:.5f})\n".format(indent, key, color, value, tcolors.ENDC, sign, diff)
        self.old_eval_loss_dict = avg_loss_dict
        print(log_text, flush=True)
