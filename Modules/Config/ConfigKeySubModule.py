
class ConfigKeySubModule:

    class ConfigKeyCommon:
        def __init__(self):
            self.check_update = 'check_update'
            self.agreed_to_disclaimer = 'agreed_to_disclaimer'
            self.recording_enable = 'recording_enable'
            self.last_running_uid = 'last_running_uid'
            self.blacklist_uid = 'blacklist_uid'
            self.cdkey_list = 'cdkey_list'
            self.next_loop_time = 'next_loop_time'
            self.multi_login_accounts = 'multi_login_accounts'
            self.want_register_accounts = 'want_register_accounts'
            self.python_exe_path = 'python_exe_path'
            self.pypi_mirror_urls = 'pypi_mirror_urls'
            self.game_title_name = 'game_title_name'
            self.game_process_name = 'game_process_name'
            self.game_path = 'game_path'
            self.power_needs = 'power_needs'
            self.universe_path = 'universe_path'
            self.universe_timeout = 'universe_timeout'
            self.universe_requirements = 'universe_requirements'
            self.hotkey_technique = 'hotkey_technique'
            self.hotkey_obs_start = 'hotkey_obs_start'
            self.hotkey_obs_stop = 'hotkey_obs_stop'
            self.notify_smtp_enable = 'notify_smtp_enable'
            self.notify_smtp_host = 'notify_smtp_host'
            self.notify_smtp_user = 'notify_smtp_user'
            self.notify_smtp_password = 'notify_smtp_password'
            self.notify_smtp_From = 'notify_smtp_From'
            self.notify_smtp_To = 'notify_smtp_To'
            self.notify_smtp_port = 'notify_smtp_port'
            self.notify_smtp_ssl = 'notify_smtp_ssl'
            self.notify_smtp_master = 'notify_smtp_master'

    class ConfigKeyUid:
        def __init__(self):
            self.instance_type = 'instance_type'
            self.instance_names = 'instance_names'
            self.instance_team_enalbe = 'instance_team_enable'
            self.instance_team_number = 'instance_team_number'
            self.use_reserved_trailblaze_power = 'use_reserved_trailblaze_power'
            self.use_fuel = 'use_fuel'
            self.echo_of_war_enable = 'echo_of_war_enable'
            self.echo_of_war_timestamp = 'echo_of_war_timestamp'
            self.echo_of_war_times = 'echo_of_war_times'
            self.relic_salvage_enable = 'relic_salvage_enable'
            self.relic_salvage_5star_enable = 'relic_salvage_5star_enable'
            self.relic_salvage_4star_enable = 'relic_salvage_4star_enable'
            self.relic_salvage_5star_to_exp = 'relic_salvage_5star_to_exp'
            self.relic_threshold_count = 'relic_threshold_count'
            self.borrow_character_enable = 'borrow_character_enable'
            self.borrow_character_from = 'borrow_character_from'
            self.borrow_character = 'borrow_character'
            self.dispatch_enable = 'dispatch_enable'
            self.mail_enable = 'mail_enable'
            self.assist_enable = 'assist_enable'
            self.daily_himeko_try_enable = 'daily_himeko_try_enable'
            self.daily_tasks = 'daily_tasks'
            self.daily_tasks_score = 'daily_tasks_score'
            self.daily_tasks_fin = 'daily_tasks_fin'
            self.last_run_timestamp = 'last_run_timestamp'
            self.universe_enable = 'universe_enable'
            self.universe_bonus_enable = 'universe_bonus_enable'
            self.universe_fin = 'universe_fin'
            self.universe_score = 'universe_score'
            self.universe_count = 'universe_count'
            self.universe_timestamp = 'universe_timestamp'
            self.forgottenhall_stars = 'forgottenhall_stars'
            self.forgottenhall_levels = 'forgottenhall_levels'
            self.purefiction_stars = 'purefiction_stars'
            self.purefiction_levels = 'purefiction_levels'

    
    def __init__(self):
        self.common = self.ConfigKeyCommon()
        self.uid = self.ConfigKeyUid()
        self.email = 'email'
        self.reg_path = 'reg_path'
        self.universe_team = 'universe_team'
        self.universe_fate = 'universe_fate'
        self.universe_number = 'universe_number'
        self.universe_difficulty = 'universe_difficulty'
        self.cylax_golden = '拟造花萼（金）'
        self.cylax_crimson = '拟造花萼（赤）'
        self.shadow = '凝滞虚影'
        self.corrision = '侵蚀隧洞'
        self.echo_of_war = '历战余响'